// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

/// @title HIP.markets HYPE Vault
/// @notice Reference scaffold for pooling HYPE to back HIP.markets' own HIP-3 deployer stake.
/// @dev This contract is not audited. It models the capital-flow and accounting surface needed
/// for a production implementation, but HyperCore staking integration still needs live validation.
contract HipMarketsVault {
    enum OperatorPhase {
        Funding,
        StakeReady,
        StakeEscrowed,
        OperatorApproved,
        MarketsLive,
        WindDown,
        Slashed
    }

    IERC20 public immutable stakeAsset;
    IERC20 public immutable rewardAsset;

    string public constant name = "HIP.markets Vault Share";
    string public constant symbol = "vHIPM";
    uint8 public constant decimals = 18;
    uint256 public constant INDEX_SCALE = 1e18;

    address public owner;
    address public pendingOwner;
    address public operator;
    address public riskCouncil;
    address public deployerStakeController;

    uint256 public immutable requiredStake;
    uint256 public vaultCap;
    uint64 public withdrawalDelay;

    uint256 public totalShares;
    uint256 public allocatedStake;
    uint256 public accountedSlashLoss;
    uint256 public rewardIndex;
    uint256 public slashingReserveAccrued;
    uint256 public protocolFeesAccrued;
    OperatorPhase public operatorPhase;

    bool public depositsPaused;
    bool public withdrawalsPaused;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => uint256) public rewardIndexOf;
    mapping(address => uint256) public accruedRewards;
    mapping(address => WithdrawalRequest) public withdrawalRequests;

    struct WithdrawalRequest {
        uint256 shares;
        uint64 executableAt;
    }

    event Transfer(address indexed from, address indexed to, uint256 amount);
    event Approval(address indexed owner, address indexed spender, uint256 amount);
    event Deposit(address indexed user, uint256 assets, uint256 shares);
    event WithdrawalQueued(address indexed user, uint256 shares, uint64 executableAt);
    event WithdrawalCancelled(address indexed user, uint256 shares);
    event WithdrawalFinalized(address indexed user, uint256 shares, uint256 assets);
    event RewardsDistributed(uint256 amount, uint256 protocolFee, uint256 reserveContribution);
    event RewardsClaimed(address indexed user, uint256 amount);
    event StakeEscrowed(address indexed destination, uint256 amount);
    event StakeReturned(uint256 amount);
    event SlashLossRecorded(uint256 amount, OperatorPhase phase);
    event OperatorPhaseUpdated(OperatorPhase oldPhase, OperatorPhase newPhase, string note);
    event PauseUpdated(bool depositsPaused, bool withdrawalsPaused);
    event OperatorUpdated(address indexed operator);
    event RiskCouncilUpdated(address indexed riskCouncil);
    event DeployerStakeControllerUpdated(address indexed controller);
    event VaultCapUpdated(uint256 oldCap, uint256 newCap);
    event WithdrawalDelayUpdated(uint64 oldDelay, uint64 newDelay);
    event OwnershipTransferStarted(address indexed oldOwner, address indexed pendingOwner);
    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "ONLY_OWNER");
        _;
    }

    modifier onlyOperator() {
        require(msg.sender == operator || msg.sender == owner, "ONLY_OPERATOR");
        _;
    }

    modifier onlyRiskCouncil() {
        require(msg.sender == riskCouncil || msg.sender == owner, "ONLY_RISK_COUNCIL");
        _;
    }

    modifier nonReentrant() {
        require(_locked == 1, "REENTRANT");
        _locked = 2;
        _;
        _locked = 1;
    }

    uint256 private _locked = 1;

    constructor(
        IERC20 stakeAsset_,
        IERC20 rewardAsset_,
        address owner_,
        address operator_,
        address riskCouncil_,
        address deployerStakeController_,
        uint256 requiredStake_,
        uint256 vaultCap_,
        uint64 withdrawalDelay_
    ) {
        require(address(stakeAsset_) != address(0), "BAD_STAKE_ASSET");
        require(address(rewardAsset_) != address(0), "BAD_REWARD_ASSET");
        require(owner_ != address(0), "BAD_OWNER");
        require(operator_ != address(0), "BAD_OPERATOR");
        require(riskCouncil_ != address(0), "BAD_RISK_COUNCIL");
        require(deployerStakeController_ != address(0), "BAD_CONTROLLER");
        require(requiredStake_ > 0, "BAD_REQUIRED_STAKE");
        require(vaultCap_ >= requiredStake_, "CAP_BELOW_REQUIRED_STAKE");

        stakeAsset = stakeAsset_;
        rewardAsset = rewardAsset_;
        owner = owner_;
        operator = operator_;
        riskCouncil = riskCouncil_;
        deployerStakeController = deployerStakeController_;
        requiredStake = requiredStake_;
        vaultCap = vaultCap_;
        withdrawalDelay = withdrawalDelay_;
        operatorPhase = OperatorPhase.Funding;
    }

    function totalAssets() public view returns (uint256) {
        return stakeAsset.balanceOf(address(this)) + allocatedStake;
    }

    function liquidAssets() public view returns (uint256) {
        return stakeAsset.balanceOf(address(this));
    }

    function netAssets() public view returns (uint256) {
        return totalAssets();
    }

    function fundingProgressBps() external view returns (uint256) {
        uint256 assets = totalAssets();
        if (assets >= requiredStake) return 10_000;
        return (assets * 10_000) / requiredStake;
    }

    function previewDeposit(uint256 assets) public view returns (uint256 shares) {
        uint256 supply = totalShares;
        uint256 assetsBefore = netAssets();
        if (supply == 0 || assetsBefore == 0) return assets;
        return (assets * supply) / assetsBefore;
    }

    function previewRedeem(uint256 shares) public view returns (uint256 assets) {
        uint256 supply = totalShares;
        if (supply == 0) return 0;
        return (shares * netAssets()) / supply;
    }

    function deposit(uint256 assets) external nonReentrant returns (uint256 shares) {
        require(!depositsPaused, "DEPOSITS_PAUSED");
        require(operatorPhase == OperatorPhase.Funding || operatorPhase == OperatorPhase.StakeReady, "DEPOSITS_CLOSED");
        require(assets > 0, "ZERO_ASSETS");
        require(totalAssets() + assets <= vaultCap, "CAP_EXCEEDED");

        _checkpoint(msg.sender);
        shares = previewDeposit(assets);
        require(shares > 0, "ZERO_SHARES");

        totalShares += shares;
        balanceOf[msg.sender] += shares;
        emit Transfer(address(0), msg.sender, shares);

        _safeTransferFrom(stakeAsset, msg.sender, address(this), assets);
        emit Deposit(msg.sender, assets, shares);

        if (operatorPhase == OperatorPhase.Funding && totalAssets() >= requiredStake) {
            _setOperatorPhase(OperatorPhase.StakeReady, "required stake funded");
        }
    }

    function queueWithdrawal(uint256 shares) external nonReentrant {
        require(!withdrawalsPaused, "WITHDRAWALS_PAUSED");
        require(shares > 0, "ZERO_SHARES");
        require(balanceOf[msg.sender] >= shares, "INSUFFICIENT_SHARES");
        require(withdrawalRequests[msg.sender].shares == 0, "REQUEST_EXISTS");
        require(operatorPhase != OperatorPhase.StakeEscrowed && operatorPhase != OperatorPhase.OperatorApproved, "STAKE_LOCKED");

        _checkpoint(msg.sender);
        balanceOf[msg.sender] -= shares;

        uint64 executableAt = uint64(block.timestamp + withdrawalDelay);
        withdrawalRequests[msg.sender] = WithdrawalRequest({
            shares: shares,
            executableAt: executableAt
        });

        emit Transfer(msg.sender, address(this), shares);
        emit WithdrawalQueued(msg.sender, shares, executableAt);
    }

    function cancelWithdrawal() external nonReentrant {
        WithdrawalRequest memory request = withdrawalRequests[msg.sender];
        require(request.shares > 0, "NO_REQUEST");

        delete withdrawalRequests[msg.sender];
        balanceOf[msg.sender] += request.shares;
        emit Transfer(address(this), msg.sender, request.shares);
        emit WithdrawalCancelled(msg.sender, request.shares);
    }

    function finalizeWithdrawal() external nonReentrant returns (uint256 assets) {
        WithdrawalRequest memory request = withdrawalRequests[msg.sender];
        require(request.shares > 0, "NO_REQUEST");
        require(block.timestamp >= request.executableAt, "NOT_READY");

        delete withdrawalRequests[msg.sender];
        assets = previewRedeem(request.shares);
        totalShares -= request.shares;
        require(assets <= liquidAssets(), "INSUFFICIENT_LIQUIDITY");

        emit Transfer(address(this), address(0), request.shares);
        _safeTransfer(stakeAsset, msg.sender, assets);
        emit WithdrawalFinalized(msg.sender, request.shares, assets);
    }

    function distributeRewards(
        uint256 amount,
        uint256 protocolFee,
        uint256 reserveContribution
    ) external onlyOperator nonReentrant {
        require(amount > 0, "ZERO_AMOUNT");
        require(totalShares > 0, "NO_SHARES");
        require(amount >= protocolFee + reserveContribution, "FEES_TOO_HIGH");

        _safeTransferFrom(rewardAsset, msg.sender, address(this), amount);
        uint256 distributable = amount - protocolFee - reserveContribution;
        protocolFeesAccrued += protocolFee;
        slashingReserveAccrued += reserveContribution;
        rewardIndex += (distributable * INDEX_SCALE) / totalShares;
        emit RewardsDistributed(distributable, protocolFee, reserveContribution);
    }

    function claimRewards() external nonReentrant returns (uint256 amount) {
        _checkpoint(msg.sender);
        amount = accruedRewards[msg.sender];
        require(amount > 0, "NO_REWARDS");

        accruedRewards[msg.sender] = 0;
        _safeTransfer(rewardAsset, msg.sender, amount);
        emit RewardsClaimed(msg.sender, amount);
    }

    function escrowStakeToController(uint256 amount, string calldata note) external onlyOwner nonReentrant {
        require(operatorPhase == OperatorPhase.StakeReady, "NOT_READY");
        require(amount >= requiredStake, "BELOW_REQUIRED_STAKE");
        require(amount <= liquidAssets(), "INSUFFICIENT_LIQUIDITY");

        allocatedStake += amount;
        _safeTransfer(stakeAsset, deployerStakeController, amount);
        emit StakeEscrowed(deployerStakeController, amount);
        _setOperatorPhase(OperatorPhase.StakeEscrowed, note);
    }

    function recordOperatorApproved(string calldata note) external onlyRiskCouncil {
        require(operatorPhase == OperatorPhase.StakeEscrowed, "STAKE_NOT_ESCROWED");
        _setOperatorPhase(OperatorPhase.OperatorApproved, note);
    }

    function recordMarketsLive(string calldata note) external onlyRiskCouncil {
        require(operatorPhase == OperatorPhase.OperatorApproved, "NOT_APPROVED");
        _setOperatorPhase(OperatorPhase.MarketsLive, note);
    }

    function beginWindDown(string calldata note) external onlyRiskCouncil {
        require(operatorPhase != OperatorPhase.Slashed, "SLASHED");
        depositsPaused = true;
        _setOperatorPhase(OperatorPhase.WindDown, note);
        emit PauseUpdated(depositsPaused, withdrawalsPaused);
    }

    function recordStakeReturned(uint256 amount, string calldata note) external onlyOwner {
        require(amount > 0, "ZERO_AMOUNT");
        require(allocatedStake >= amount, "TOO_MUCH");
        allocatedStake -= amount;
        emit StakeReturned(amount);
        if (operatorPhase == OperatorPhase.WindDown && allocatedStake == 0) {
            _setOperatorPhase(OperatorPhase.Funding, note);
        }
    }

    function recordSlashLoss(uint256 amount, string calldata note) external onlyRiskCouncil {
        require(amount > 0, "ZERO_AMOUNT");
        accountedSlashLoss += amount;
        if (amount >= allocatedStake) {
            allocatedStake = 0;
        } else {
            allocatedStake -= amount;
        }
        _setOperatorPhase(OperatorPhase.Slashed, note);
        emit SlashLossRecorded(amount, operatorPhase);
    }

    function setPause(bool depositsPaused_, bool withdrawalsPaused_) external onlyRiskCouncil {
        depositsPaused = depositsPaused_;
        withdrawalsPaused = withdrawalsPaused_;
        emit PauseUpdated(depositsPaused_, withdrawalsPaused_);
    }

    function setVaultCap(uint256 vaultCap_) external onlyOwner {
        require(vaultCap_ >= requiredStake, "CAP_BELOW_REQUIRED_STAKE");
        emit VaultCapUpdated(vaultCap, vaultCap_);
        vaultCap = vaultCap_;
    }

    function setWithdrawalDelay(uint64 withdrawalDelay_) external onlyOwner {
        emit WithdrawalDelayUpdated(withdrawalDelay, withdrawalDelay_);
        withdrawalDelay = withdrawalDelay_;
    }

    function setOperator(address operator_) external onlyOwner {
        require(operator_ != address(0), "BAD_OPERATOR");
        operator = operator_;
        emit OperatorUpdated(operator_);
    }

    function setRiskCouncil(address riskCouncil_) external onlyOwner {
        require(riskCouncil_ != address(0), "BAD_RISK_COUNCIL");
        riskCouncil = riskCouncil_;
        emit RiskCouncilUpdated(riskCouncil_);
    }

    function setDeployerStakeController(address controller_) external onlyOwner {
        require(controller_ != address(0), "BAD_CONTROLLER");
        deployerStakeController = controller_;
        emit DeployerStakeControllerUpdated(controller_);
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 allowed = allowance[from][msg.sender];
        require(allowed >= amount, "ALLOWANCE");
        if (allowed != type(uint256).max) {
            allowance[from][msg.sender] = allowed - amount;
            emit Approval(from, msg.sender, allowance[from][msg.sender]);
        }
        _transfer(from, to, amount);
        return true;
    }

    function pendingRewards(address user) external view returns (uint256) {
        uint256 delta = rewardIndex - rewardIndexOf[user];
        return accruedRewards[user] + ((balanceOf[user] * delta) / INDEX_SCALE);
    }

    function startOwnershipTransfer(address newOwner) external onlyOwner {
        require(newOwner != address(0), "BAD_OWNER");
        pendingOwner = newOwner;
        emit OwnershipTransferStarted(owner, newOwner);
    }

    function acceptOwnership() external {
        require(msg.sender == pendingOwner, "ONLY_PENDING_OWNER");
        address oldOwner = owner;
        owner = pendingOwner;
        pendingOwner = address(0);
        emit OwnershipTransferred(oldOwner, owner);
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(to != address(0), "BAD_RECIPIENT");
        require(balanceOf[from] >= amount, "INSUFFICIENT_BALANCE");
        _checkpoint(from);
        _checkpoint(to);
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _checkpoint(address user) internal {
        uint256 delta = rewardIndex - rewardIndexOf[user];
        if (delta > 0) {
            accruedRewards[user] += (balanceOf[user] * delta) / INDEX_SCALE;
        }
        rewardIndexOf[user] = rewardIndex;
    }

    function _setOperatorPhase(OperatorPhase phase, string memory note) internal {
        OperatorPhase oldPhase = operatorPhase;
        operatorPhase = phase;
        emit OperatorPhaseUpdated(oldPhase, phase, note);
    }

    function _safeTransfer(IERC20 token, address to, uint256 amount) internal {
        (bool success, bytes memory data) = address(token).call(
            abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool))), "TRANSFER_FAILED");
    }

    function _safeTransferFrom(IERC20 token, address from, address to, uint256 amount) internal {
        (bool success, bytes memory data) = address(token).call(
            abi.encodeWithSelector(IERC20.transferFrom.selector, from, to, amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool))), "TRANSFER_FROM_FAILED");
    }
}
