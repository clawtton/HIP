# Oracle Operations Plan

## Why Oracles Are The Core Operating Risk

HIP-3 markets are builder-operated. The builder is responsible for publishing prices. For HIP.markets, this means user HYPE is not just backing a vault; it is backing the team's ability to operate reliable price infrastructure.

Bad oracle behavior can cause:

- unfair liquidations;
- stale markets;
- manipulation;
- trading halts;
- slash risk;
- reputational loss;
- legal exposure.

## MVP Oracle Strategy

Start with markets where oracle infrastructure is easiest to defend:

- strong public price feeds;
- high-liquidity reference venues;
- multiple independent data sources;
- simple trading sessions;
- low holiday/roll complexity.

Avoid early markets that require:

- complex futures rolls;
- branded index licenses;
- illiquid regional equities;
- bespoke off-hours pricing;
- weak or single-source data.

## Relayer Requirements

The relayer system should provide:

- approximately three-second update cadence;
- active-active or active-passive redundancy;
- price staleness detection;
- data-source quorum;
- deviation checks;
- signer separation;
- monitoring dashboards;
- incident alerts;
- manual halt procedures.

## Data Source Hierarchy

Tier 1:

- Pyth or equivalent high-quality feeds;
- major exchange data;
- institutional quote sources;
- direct data vendor feeds.

Tier 2:

- secondary exchange feeds;
- backup aggregators;
- market-maker quotes;
- TWAP/VWAP derived feeds.

Tier 3:

- internal orderbook-based discovery, only with explicit bounds and disclosure.

## Health Metrics

The dashboard should display:

- last update timestamp;
- median update interval;
- missed update count;
- stale duration;
- reference price;
- oracle price;
- mark price;
- deviation in bps;
- data source count;
- degraded/normal state.

## Incident Levels

Green:

- all sources normal;
- update cadence normal;
- deviation within threshold.

Yellow:

- one source degraded;
- update cadence slightly delayed;
- deposits remain open.

Orange:

- stale price or large deviation;
- pause deposits;
- keep withdrawals open if safe.

Red:

- oracle failure or suspected manipulation;
- pause deposits;
- consider market halt;
- risk committee review.

## First Three Market Recommendation

The first three markets should optimize for operational safety:

1. A crypto major with redundant public feeds.
2. A second liquid crypto or HYPE-adjacent market.
3. A simple, highly liquid RWA only if feed and licensing are clear.

The first launch should prove uptime, fee routing, and risk controls before expanding into trade.xyz-style equities, commodities, or indices.
