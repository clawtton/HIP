// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title HIP.markets Registry
/// @notice Public metadata registry for HIP.markets-operated HIP-3 markets, stake lifecycle,
/// oracle health, fee epochs, and risk state.
contract HipMarketsRegistry {
    enum OperatorStatus {
        Draft,
        Funding,
        StakeReady,
        StakeSubmitted,
        Approved,
        Live,
        Halted,
        WindDown
    }

    enum MarketStatus {
        Proposed,
        OracleReview,
        MakerReview,
        Ready,
        Live,
        Halted,
        Settled,
        Delisted
    }

    enum RiskState {
        Green,
        Watch,
        Red,
        Frozen
    }

    address public owner;
    address public pendingOwner;
    address public riskCouncil;
    address public oracleReporter;
    address public feeReporter;

    struct DexConfig {
        address deployer;
        address oracleUpdater;
        address feeRecipient;
        address vault;
        string dexName;
        string disclosureUri;
        uint256 requiredStake;
        uint256 stakedHype;
        uint256 deployerFeeScaleBps;
        OperatorStatus status;
        RiskState riskState;
        bool active;
    }

    struct MarketConfig {
        string symbol;
        string category;
        string oracleMethodologyUri;
        string dataSourcesUri;
        uint256 maxOpenInterestUsd;
        uint256 maxLeverage;
        uint256 initialMarginBps;
        uint256 maintenanceMarginBps;
        bool growthMode;
        MarketStatus status;
        RiskState riskState;
    }

    struct OracleHealth {
        uint64 lastUpdate;
        uint64 updateIntervalSeconds;
        uint64 staleAfterSeconds;
        int256 lastDeviationBps;
        int256 maxDeviationBps;
        bool degraded;
        string note;
    }

    struct FeeEpoch {
        uint64 startTime;
        uint64 endTime;
        uint256 volumeUsd;
        uint256 grossTradingFees;
        uint256 deployerFees;
        uint256 operatingCost;
        uint256 reserveContribution;
        uint256 distributedRewards;
        string reportUri;
        bool finalized;
    }

    struct LaunchChecklist {
        bool stakeFunded;
        bool hyperCoreStakeSubmitted;
        bool operatorApproved;
        bool oracleRunbookPublished;
        bool makerCommitmentsSigned;
        bool feeRecipientVerified;
        bool emergencyPlanReady;
    }

    DexConfig public dexConfig;
    LaunchChecklist public launchChecklist;
    mapping(bytes32 => MarketConfig) public markets;
    mapping(bytes32 => OracleHealth) public oracleHealth;
    mapping(uint256 => FeeEpoch) public feeEpochs;
    bytes32[] public marketIds;
    uint256 public nextFeeEpochId = 1;

    event DexConfigUpdated(address deployer, address oracleUpdater, address feeRecipient, address vault, string dexName);
    event OperatorStatusUpdated(OperatorStatus status, RiskState riskState, string note);
    event LaunchChecklistUpdated(LaunchChecklist checklist);
    event MarketUpdated(bytes32 indexed marketId, string symbol, MarketStatus status, RiskState riskState);
    event OracleHealthUpdated(bytes32 indexed marketId, uint64 lastUpdate, bool degraded, string note);
    event FeeEpochPublished(uint256 indexed epochId, uint256 deployerFees, uint256 distributedRewards, bool finalized);
    event RiskCouncilUpdated(address indexed riskCouncil);
    event OracleReporterUpdated(address indexed oracleReporter);
    event FeeReporterUpdated(address indexed feeReporter);
    event OwnershipTransferStarted(address indexed oldOwner, address indexed pendingOwner);
    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "ONLY_OWNER");
        _;
    }

    modifier onlyRiskCouncil() {
        require(msg.sender == riskCouncil || msg.sender == owner, "ONLY_RISK_COUNCIL");
        _;
    }

    modifier onlyOracleReporter() {
        require(msg.sender == oracleReporter || msg.sender == riskCouncil || msg.sender == owner, "ONLY_ORACLE_REPORTER");
        _;
    }

    modifier onlyFeeReporter() {
        require(msg.sender == feeReporter || msg.sender == riskCouncil || msg.sender == owner, "ONLY_FEE_REPORTER");
        _;
    }

    constructor(address owner_, address riskCouncil_, address oracleReporter_, address feeReporter_) {
        require(owner_ != address(0), "BAD_OWNER");
        require(riskCouncil_ != address(0), "BAD_RISK_COUNCIL");
        require(oracleReporter_ != address(0), "BAD_ORACLE_REPORTER");
        require(feeReporter_ != address(0), "BAD_FEE_REPORTER");
        owner = owner_;
        riskCouncil = riskCouncil_;
        oracleReporter = oracleReporter_;
        feeReporter = feeReporter_;
    }

    function setDexConfig(DexConfig calldata config) external onlyOwner {
        require(config.deployer != address(0), "BAD_DEPLOYER");
        require(config.oracleUpdater != address(0), "BAD_ORACLE");
        require(config.feeRecipient != address(0), "BAD_FEE_RECIPIENT");
        require(config.vault != address(0), "BAD_VAULT");
        require(config.requiredStake > 0, "BAD_REQUIRED_STAKE");
        dexConfig = config;
        emit DexConfigUpdated(config.deployer, config.oracleUpdater, config.feeRecipient, config.vault, config.dexName);
    }

    function setOperatorStatus(
        OperatorStatus status,
        RiskState riskState,
        uint256 stakedHype,
        string calldata note
    ) external onlyRiskCouncil {
        dexConfig.status = status;
        dexConfig.riskState = riskState;
        dexConfig.stakedHype = stakedHype;
        emit OperatorStatusUpdated(status, riskState, note);
    }

    function setLaunchChecklist(LaunchChecklist calldata checklist) external onlyRiskCouncil {
        launchChecklist = checklist;
        emit LaunchChecklistUpdated(checklist);
    }

    function setMarket(MarketConfig calldata config) external onlyRiskCouncil returns (bytes32 marketId) {
        require(bytes(config.symbol).length > 0, "BAD_SYMBOL");
        require(config.maxLeverage > 0, "BAD_LEVERAGE");
        require(config.maxOpenInterestUsd > 0, "BAD_OI_CAP");
        marketId = keccak256(bytes(config.symbol));

        if (bytes(markets[marketId].symbol).length == 0) {
            marketIds.push(marketId);
        }

        markets[marketId] = config;
        emit MarketUpdated(marketId, config.symbol, config.status, config.riskState);
    }

    function setOracleHealth(bytes32 marketId, OracleHealth calldata health) external onlyOracleReporter {
        require(bytes(markets[marketId].symbol).length > 0, "UNKNOWN_MARKET");
        require(health.updateIntervalSeconds > 0, "BAD_INTERVAL");
        require(health.staleAfterSeconds >= health.updateIntervalSeconds, "BAD_STALE_AFTER");
        oracleHealth[marketId] = health;
        emit OracleHealthUpdated(marketId, health.lastUpdate, health.degraded, health.note);
    }

    function publishFeeEpoch(FeeEpoch calldata epoch) external onlyFeeReporter returns (uint256 epochId) {
        require(epoch.endTime >= epoch.startTime, "BAD_EPOCH");
        require(epoch.deployerFees >= epoch.reserveContribution + epoch.distributedRewards, "BAD_FEE_SPLIT");
        epochId = nextFeeEpochId++;
        feeEpochs[epochId] = epoch;
        emit FeeEpochPublished(epochId, epoch.deployerFees, epoch.distributedRewards, epoch.finalized);
    }

    function marketCount() external view returns (uint256) {
        return marketIds.length;
    }

    function setRiskCouncil(address riskCouncil_) external onlyOwner {
        require(riskCouncil_ != address(0), "BAD_RISK_COUNCIL");
        riskCouncil = riskCouncil_;
        emit RiskCouncilUpdated(riskCouncil_);
    }

    function setOracleReporter(address oracleReporter_) external onlyOwner {
        require(oracleReporter_ != address(0), "BAD_ORACLE_REPORTER");
        oracleReporter = oracleReporter_;
        emit OracleReporterUpdated(oracleReporter_);
    }

    function setFeeReporter(address feeReporter_) external onlyOwner {
        require(feeReporter_ != address(0), "BAD_FEE_REPORTER");
        feeReporter = feeReporter_;
        emit FeeReporterUpdated(feeReporter_);
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
}
