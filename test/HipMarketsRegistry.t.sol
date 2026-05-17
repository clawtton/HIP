// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/HipMarketsRegistry.sol";

interface RegistryVm {
    function prank(address sender) external;
}

contract RegistryTestBase {
    RegistryVm internal constant vm = RegistryVm(address(uint160(uint256(keccak256("hevm cheat code")))));

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

contract HipMarketsRegistryTest is RegistryTestBase {
    HipMarketsRegistry internal registry;

    address internal owner = address(0x2001);
    address internal riskCouncil = address(0x2002);
    address internal oracleReporter = address(0x2003);
    address internal feeReporter = address(0x2004);
    address internal deployer = address(0x2005);
    address internal oracleUpdater = address(0x2006);
    address internal feeRecipient = address(0x2007);
    address internal vault = address(0x2008);

    function setUp() public {
        registry = new HipMarketsRegistry(owner, riskCouncil, oracleReporter, feeReporter);
    }

    function testDexConfigAndOperatorStatus() public {
        HipMarketsRegistry.DexConfig memory config = HipMarketsRegistry.DexConfig({
            deployer: deployer,
            oracleUpdater: oracleUpdater,
            feeRecipient: feeRecipient,
            vault: vault,
            dexName: "hipm",
            disclosureUri: "ipfs://disclosure",
            requiredStake: 500_000e18,
            stakedHype: 0,
            deployerFeeScaleBps: 10_000,
            status: HipMarketsRegistry.OperatorStatus.Funding,
            riskState: HipMarketsRegistry.RiskState.Green,
            active: true
        });

        vm.prank(owner);
        registry.setDexConfig(config);

        (address storedDeployer,, address storedFeeRecipient,,,, uint256 requiredStake,,,,,) = registry.dexConfig();
        assertEq(storedDeployer, deployer, "deployer");
        assertEq(storedFeeRecipient, feeRecipient, "fee recipient");
        assertEq(requiredStake, 500_000e18, "required stake");

        vm.prank(riskCouncil);
        registry.setOperatorStatus(
            HipMarketsRegistry.OperatorStatus.Live,
            HipMarketsRegistry.RiskState.Watch,
            500_000e18,
            "live but watched"
        );

        (,,,,,,,,, HipMarketsRegistry.OperatorStatus status, HipMarketsRegistry.RiskState riskState,) = registry.dexConfig();
        assertEq(uint256(status), uint256(HipMarketsRegistry.OperatorStatus.Live), "status");
        assertEq(uint256(riskState), uint256(HipMarketsRegistry.RiskState.Watch), "risk");
    }

    function testMarketOracleHealthAndFeeEpochReporting() public {
        HipMarketsRegistry.MarketConfig memory market = HipMarketsRegistry.MarketConfig({
            symbol: "hipm:HYPE",
            category: "crypto major",
            oracleMethodologyUri: "ipfs://oracle",
            dataSourcesUri: "ipfs://sources",
            maxOpenInterestUsd: 10_000_000e18,
            maxLeverage: 10,
            initialMarginBps: 1_000,
            maintenanceMarginBps: 500,
            growthMode: false,
            status: HipMarketsRegistry.MarketStatus.Ready,
            riskState: HipMarketsRegistry.RiskState.Green
        });

        vm.prank(riskCouncil);
        bytes32 marketId = registry.setMarket(market);
        assertEq(registry.marketCount(), 1, "market count");

        HipMarketsRegistry.OracleHealth memory health = HipMarketsRegistry.OracleHealth({
            lastUpdate: 1_779_000_000,
            updateIntervalSeconds: 3,
            staleAfterSeconds: 9,
            lastDeviationBps: 4,
            maxDeviationBps: 25,
            degraded: false,
            note: "healthy"
        });

        vm.prank(oracleReporter);
        registry.setOracleHealth(marketId, health);

        (uint64 lastUpdate, uint64 updateIntervalSeconds,,,, bool degraded,) = registry.oracleHealth(marketId);
        assertEq(uint256(lastUpdate), 1_779_000_000, "last update");
        assertEq(uint256(updateIntervalSeconds), 3, "interval");
        assertTrue(!degraded, "not degraded");

        HipMarketsRegistry.FeeEpoch memory epoch = HipMarketsRegistry.FeeEpoch({
            startTime: 1,
            endTime: 2,
            volumeUsd: 100_000_000e18,
            grossTradingFees: 60_000e18,
            deployerFees: 30_000e18,
            operatingCost: 6_000e18,
            reserveContribution: 3_000e18,
            distributedRewards: 18_000e18,
            reportUri: "ipfs://fee-report",
            finalized: true
        });

        vm.prank(feeReporter);
        uint256 epochId = registry.publishFeeEpoch(epoch);

        (,,, uint256 grossTradingFees, uint256 deployerFees,,, uint256 distributedRewards,, bool finalized) =
            registry.feeEpochs(epochId);
        assertEq(grossTradingFees, 60_000e18, "gross fees");
        assertEq(deployerFees, 30_000e18, "deployer fees");
        assertEq(distributedRewards, 18_000e18, "distributed rewards");
        assertTrue(finalized, "finalized");
    }

    function testUnauthorizedReporterCannotPublishFeeEpoch() public {
        HipMarketsRegistry.FeeEpoch memory epoch = HipMarketsRegistry.FeeEpoch({
            startTime: 1,
            endTime: 2,
            volumeUsd: 1,
            grossTradingFees: 1,
            deployerFees: 1,
            operatingCost: 0,
            reserveContribution: 0,
            distributedRewards: 1,
            reportUri: "ipfs://fee-report",
            finalized: true
        });

        vm.prank(address(0xBAD));
        (bool ok,) = address(registry).call(abi.encodeCall(registry.publishFeeEpoch, (epoch)));
        assertTrue(!ok, "unauthorized publish should fail");
    }
}
