// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/HipMarketsVault.sol";

interface Vm {
    function prank(address sender) external;
    function startPrank(address sender) external;
    function stopPrank() external;
    function warp(uint256 newTimestamp) external;
}

contract TestBase {
    Vm internal constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    function assertEq(uint256 actual, uint256 expected, string memory message) internal pure {
        require(actual == expected, message);
    }

    function assertEq(address actual, address expected, string memory message) internal pure {
        require(actual == expected, message);
    }

    function assertTrue(bool value, string memory message) internal pure {
        require(value, message);
    }
}

contract MockERC20 is IERC20 {
    string public name = "Mock Token";
    string public symbol = "MOCK";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public override balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) external override returns (bool) {
        require(balanceOf[msg.sender] >= amount, "BALANCE");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external override returns (bool) {
        uint256 allowed = allowance[from][msg.sender];
        require(allowed >= amount, "ALLOWANCE");
        require(balanceOf[from] >= amount, "BALANCE");
        if (allowed != type(uint256).max) {
            allowance[from][msg.sender] = allowed - amount;
        }
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

contract HipMarketsVaultTest is TestBase {
    MockERC20 internal hype;
    MockERC20 internal usdc;
    HipMarketsVault internal vault;

    address internal owner = address(0x1001);
    address internal operator = address(0x1002);
    address internal riskCouncil = address(0x1003);
    address internal controller = address(0x1004);
    address internal alice = address(0xA11CE);
    address internal bob = address(0xB0B);

    uint256 internal constant ONE = 1e18;
    uint256 internal constant REQUIRED_STAKE = 500_000e18;

    function setUp() public {
        hype = new MockERC20();
        usdc = new MockERC20();
        vault = new HipMarketsVault(
            IERC20(address(hype)),
            IERC20(address(usdc)),
            owner,
            operator,
            riskCouncil,
            controller,
            REQUIRED_STAKE,
            600_000e18,
            7 days
        );

        hype.mint(alice, 600_000e18);
        hype.mint(bob, 100_000e18);
        usdc.mint(operator, 1_000_000e18);

        vm.prank(alice);
        hype.approve(address(vault), type(uint256).max);
        vm.prank(bob);
        hype.approve(address(vault), type(uint256).max);
        vm.prank(operator);
        usdc.approve(address(vault), type(uint256).max);
    }

    function testDepositMintsReceiptSharesAndMovesToStakeReady() public {
        vm.prank(alice);
        uint256 shares = vault.deposit(REQUIRED_STAKE);

        assertEq(shares, REQUIRED_STAKE, "first deposit should mint 1:1 shares");
        assertEq(vault.balanceOf(alice), REQUIRED_STAKE, "alice shares");
        assertEq(hype.balanceOf(address(vault)), REQUIRED_STAKE, "vault liquid HYPE");
        assertEq(uint256(vault.operatorPhase()), uint256(HipMarketsVault.OperatorPhase.StakeReady), "phase");
        assertEq(vault.fundingProgressBps(), 10_000, "funding progress");
    }

    function testLaterDepositMintsProportionalSharesAfterRewards() public {
        vm.prank(alice);
        vault.deposit(100_000e18);

        vm.prank(operator);
        vault.distributeRewards(1_000e18, 100e18, 100e18);

        vm.prank(bob);
        uint256 shares = vault.deposit(100_000e18);

        assertEq(shares, 100_000e18, "reward asset should not change HYPE share price");
        assertEq(vault.totalShares(), 200_000e18, "total shares");
    }

    function testRewardCheckpointingOnShareTransfer() public {
        vm.prank(alice);
        vault.deposit(100_000e18);

        vm.prank(operator);
        vault.distributeRewards(1_000e18, 100e18, 100e18);

        vm.prank(alice);
        vault.transfer(bob, 40_000e18);

        assertEq(vault.pendingRewards(alice), 800e18, "alice keeps accrued reward before transfer");
        assertEq(vault.pendingRewards(bob), 0, "bob does not get old reward");

        vm.prank(operator);
        vault.distributeRewards(500e18, 0, 0);

        assertEq(vault.pendingRewards(alice), 1_100e18, "alice receives future reward on remaining shares");
        assertEq(vault.pendingRewards(bob), 200e18, "bob receives future reward on transferred shares");
    }

    function testWithdrawalQueueCancelAndFinalize() public {
        vm.prank(alice);
        vault.deposit(100_000e18);

        vm.prank(alice);
        vault.queueWithdrawal(25_000e18);
        assertEq(vault.balanceOf(alice), 75_000e18, "shares queued");

        vm.prank(alice);
        vault.cancelWithdrawal();
        assertEq(vault.balanceOf(alice), 100_000e18, "shares restored");

        vm.prank(alice);
        vault.queueWithdrawal(25_000e18);
        vm.warp(block.timestamp + 7 days + 1);

        uint256 beforeBalance = hype.balanceOf(alice);
        vm.prank(alice);
        uint256 assets = vault.finalizeWithdrawal();

        assertEq(assets, 25_000e18, "withdraw assets");
        assertEq(hype.balanceOf(alice), beforeBalance + 25_000e18, "alice received HYPE");
        assertEq(vault.totalShares(), 75_000e18, "shares burned");
    }

    function testStakeEscrowPhaseAndWithdrawalLock() public {
        vm.prank(alice);
        vault.deposit(REQUIRED_STAKE);

        vm.prank(owner);
        vault.escrowStakeToController(REQUIRED_STAKE, "submit stake");

        assertEq(hype.balanceOf(controller), REQUIRED_STAKE, "controller received stake");
        assertEq(vault.allocatedStake(), REQUIRED_STAKE, "allocated stake");
        assertEq(uint256(vault.operatorPhase()), uint256(HipMarketsVault.OperatorPhase.StakeEscrowed), "escrow phase");

        vm.prank(riskCouncil);
        vault.recordOperatorApproved("approved");
        vm.prank(riskCouncil);
        vault.recordMarketsLive("live");

        assertEq(uint256(vault.operatorPhase()), uint256(HipMarketsVault.OperatorPhase.MarketsLive), "live phase");
    }

    function testSlashLossReducesAllocatedStakeAndMarksSlashed() public {
        vm.prank(alice);
        vault.deposit(REQUIRED_STAKE);
        vm.prank(owner);
        vault.escrowStakeToController(REQUIRED_STAKE, "submit stake");

        vm.prank(riskCouncil);
        vault.recordSlashLoss(125_000e18, "oracle fault");

        assertEq(vault.allocatedStake(), 375_000e18, "allocated stake after slash");
        assertEq(vault.accountedSlashLoss(), 125_000e18, "slash accounting");
        assertEq(uint256(vault.operatorPhase()), uint256(HipMarketsVault.OperatorPhase.Slashed), "slashed phase");
    }

    function testOnlyRiskCouncilCanPause() public {
        vm.prank(alice);
        (bool ok,) = address(vault).call(abi.encodeCall(vault.setPause, (true, true)));
        assertTrue(!ok, "alice cannot pause");

        vm.prank(riskCouncil);
        vault.setPause(true, true);
        assertTrue(vault.depositsPaused(), "deposits paused");
        assertTrue(vault.withdrawalsPaused(), "withdrawals paused");
    }
}

