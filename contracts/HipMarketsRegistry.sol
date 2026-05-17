// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title HIP.markets Registry
/// @notice Public metadata registry for HIP.markets-operated HIP-3 markets.
contract HipMarketsRegistry {
    address public owner;

    struct DexConfig {
        address deployer;
        address oracleUpdater;
        address feeRecipient;
        string dexName;
        string disclosureUri;
        bool active;
    }

    struct MarketConfig {
        string symbol;
        string category;
        string oracleMethodologyUri;
        uint256 maxOpenInterestUsd;
        uint256 maxLeverage;
        bool growthMode;
        bool active;
    }

    struct OracleHealth {
        uint64 lastUpdate;
        uint64 updateIntervalSeconds;
        int256 lastDeviationBps;
        bool degraded;
    }

    DexConfig public dexConfig;
    mapping(bytes32 => MarketConfig) public markets;
    mapping(bytes32 => OracleHealth) public oracleHealth;
    bytes32[] public marketIds;

    event DexConfigUpdated(address deployer, address oracleUpdater, address feeRecipient, string dexName);
    event MarketUpdated(bytes32 indexed marketId, string symbol, string category, bool active);
    event OracleHealthUpdated(bytes32 indexed marketId, uint64 lastUpdate, bool degraded);
    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "ONLY_OWNER");
        _;
    }

    constructor(address owner_) {
        require(owner_ != address(0), "BAD_OWNER");
        owner = owner_;
    }

    function setDexConfig(DexConfig calldata config) external onlyOwner {
        require(config.deployer != address(0), "BAD_DEPLOYER");
        require(config.oracleUpdater != address(0), "BAD_ORACLE");
        require(config.feeRecipient != address(0), "BAD_FEE_RECIPIENT");
        dexConfig = config;
        emit DexConfigUpdated(config.deployer, config.oracleUpdater, config.feeRecipient, config.dexName);
    }

    function setMarket(MarketConfig calldata config) external onlyOwner returns (bytes32 marketId) {
        require(bytes(config.symbol).length > 0, "BAD_SYMBOL");
        marketId = keccak256(bytes(config.symbol));

        if (bytes(markets[marketId].symbol).length == 0) {
            marketIds.push(marketId);
        }

        markets[marketId] = config;
        emit MarketUpdated(marketId, config.symbol, config.category, config.active);
    }

    function setOracleHealth(bytes32 marketId, OracleHealth calldata health) external onlyOwner {
        require(bytes(markets[marketId].symbol).length > 0, "UNKNOWN_MARKET");
        oracleHealth[marketId] = health;
        emit OracleHealthUpdated(marketId, health.lastUpdate, health.degraded);
    }

    function marketCount() external view returns (uint256) {
        return marketIds.length;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "BAD_OWNER");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
