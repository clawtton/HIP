// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

/// @title HIP.markets HYPE Vault
/// @notice Reference scaffold for pooling HYPE to back HIP.markets' own HIP-3 deployer stake.
/// @dev This contract is not audited. It is intended for hackathon review and architecture discussion.
contract HipMarketsVault {
    IERC20 public immutable stakeAsset;
    IERC20 public immutable rewardAsset;

    address public owner;
    address public operator;
    address public deployerStakeController;

    uint256 public totalShares;
    uint256 public allocatedStake;
    uint256 public accountedSlashLoss;
    uint256 public rewardIndex;
    uint256 public constant INDEX_SCALE = 1e18;

    bool public depositsPaused;
    bool public withdrawalsPaused;

    mapping(address => uint256) public sharesOf;
    mapping(address => uint256) public rewardIndexOf;
    mapping(address => uint256) public accruedRewards;
    mapping(address => WithdrawalRequest) public withdrawalRequests;

    struct WithdrawalRequest {
        uint256 shares;
        uint64 executableAt;
    }

    event Deposit(address indexed user, uint256 assets, uint256 shares);
    event WithdrawalQueued(address indexed user, uint256 shares, uint64 executableAt);
    event WithdrawalFinalized(address indexed user, uint256 shares, uint256 assets);
    event RewardsDistributed(uint256 amount);
    event StakeAllocated(address indexed destination, uint256 amount);
    event StakeReturned(uint256 amount);
    event SlashLossRecorded(uint256 amount);
    event PauseUpdated(bool depositsPaused, bool withdrawalsPaused);
    event OperatorUpdated(address indexed operator);
    event DeployerStakeControllerUpdated(address indexed controller);

    modifier onlyOwner() {
        require(msg.sender == owner, "ONLY_OWNER");
        _;
    }

    modifier onlyOperator() {
        require(msg.sender == operator || msg.sender == owner, "ONLY_OPERATOR");
        _;
    }

    constructor(
        IERC20 stakeAsset_,
        IERC20 rewardAsset_,
        address owner_,
        address operator_,
        address deployerStakeController_
    ) {
        require(address(stakeAsset_) != address(0), "BAD_STAKE_ASSET");
        require(address(rewardAsset_) != address(0), "BAD_REWARD_ASSET");
        require(owner_ != address(0), "BAD_OWNER");
        require(operator_ != address(0), "BAD_OPERATOR");
        require(deployerStakeController_ != address(0), "BAD_CONTROLLER");

        stakeAsset = stakeAsset_;
        rewardAsset = rewardAsset_;
        owner = owner_;
        operator = operator_;
        deployerStakeController = deployerStakeController_;
    }

    function deposit(uint256 assets) external returns (uint256 shares) {
        require(!depositsPaused, "DEPOSITS_PAUSED");
        require(assets > 0, "ZERO_ASSETS");

        _checkpoint(msg.sender);
        shares = assets;
        totalShares += shares;
        sharesOf[msg.sender] += shares;

        require(stakeAsset.transferFrom(msg.sender, address(this), assets), "TRANSFER_FAILED");
        emit Deposit(msg.sender, assets, shares);
    }

    function queueWithdrawal(uint256 shares, uint64 delaySeconds) external {
        require(!withdrawalsPaused, "WITHDRAWALS_PAUSED");
        require(shares > 0, "ZERO_SHARES");
        require(sharesOf[msg.sender] >= shares, "INSUFFICIENT_SHARES");
        require(withdrawalRequests[msg.sender].shares == 0, "REQUEST_EXISTS");

        _checkpoint(msg.sender);
        sharesOf[msg.sender] -= shares;

        uint64 executableAt = uint64(block.timestamp + delaySeconds);
        withdrawalRequests[msg.sender] = WithdrawalRequest({
            shares: shares,
            executableAt: executableAt
        });

        emit WithdrawalQueued(msg.sender, shares, executableAt);
    }

    function finalizeWithdrawal() external returns (uint256 assets) {
        WithdrawalRequest memory request = withdrawalRequests[msg.sender];
        require(request.shares > 0, "NO_REQUEST");
        require(block.timestamp >= request.executableAt, "NOT_READY");

        delete withdrawalRequests[msg.sender];
        totalShares -= request.shares;
        assets = request.shares;

        require(stakeAsset.transfer(msg.sender, assets), "TRANSFER_FAILED");
        emit WithdrawalFinalized(msg.sender, request.shares, assets);
    }

    function distributeRewards(uint256 amount) external onlyOperator {
        require(amount > 0, "ZERO_AMOUNT");
        require(totalShares > 0, "NO_SHARES");
        require(rewardAsset.transferFrom(msg.sender, address(this), amount), "TRANSFER_FAILED");

        rewardIndex += (amount * INDEX_SCALE) / totalShares;
        emit RewardsDistributed(amount);
    }

    function claimRewards() external returns (uint256 amount) {
        _checkpoint(msg.sender);
        amount = accruedRewards[msg.sender];
        require(amount > 0, "NO_REWARDS");

        accruedRewards[msg.sender] = 0;
        require(rewardAsset.transfer(msg.sender, amount), "TRANSFER_FAILED");
    }

    function allocateStake(uint256 amount) external onlyOwner {
        require(amount > 0, "ZERO_AMOUNT");
        allocatedStake += amount;
        require(stakeAsset.transfer(deployerStakeController, amount), "TRANSFER_FAILED");
        emit StakeAllocated(deployerStakeController, amount);
    }

    function recordStakeReturned(uint256 amount) external onlyOwner {
        require(amount > 0, "ZERO_AMOUNT");
        require(allocatedStake >= amount, "TOO_MUCH");
        allocatedStake -= amount;
        emit StakeReturned(amount);
    }

    function recordSlashLoss(uint256 amount) external onlyOwner {
        require(amount > 0, "ZERO_AMOUNT");
        accountedSlashLoss += amount;
        emit SlashLossRecorded(amount);
    }

    function setPause(bool depositsPaused_, bool withdrawalsPaused_) external onlyOwner {
        depositsPaused = depositsPaused_;
        withdrawalsPaused = withdrawalsPaused_;
        emit PauseUpdated(depositsPaused_, withdrawalsPaused_);
    }

    function setOperator(address operator_) external onlyOwner {
        require(operator_ != address(0), "BAD_OPERATOR");
        operator = operator_;
        emit OperatorUpdated(operator_);
    }

    function setDeployerStakeController(address controller_) external onlyOwner {
        require(controller_ != address(0), "BAD_CONTROLLER");
        deployerStakeController = controller_;
        emit DeployerStakeControllerUpdated(controller_);
    }

    function pendingRewards(address user) external view returns (uint256) {
        uint256 delta = rewardIndex - rewardIndexOf[user];
        return accruedRewards[user] + ((sharesOf[user] * delta) / INDEX_SCALE);
    }

    function _checkpoint(address user) internal {
        uint256 delta = rewardIndex - rewardIndexOf[user];
        if (delta > 0) {
            accruedRewards[user] += (sharesOf[user] * delta) / INDEX_SCALE;
            rewardIndexOf[user] = rewardIndex;
        }
    }
}
