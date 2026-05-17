# HIP.markets Pitch Deck

## Slide 1: Title

**HIP.markets**

Community-backed HIP-3 markets on Hyperliquid.

Pool HYPE. Launch markets. Share builder fees.

## Slide 2: The Problem

HIP-3 lets builders launch custom perpetual DEXs, but one DEX requires 500,000 HYPE staked.

That creates a bottleneck:

- builders need large HYPE backing;
- HYPE holders want market-growth yield;
- users need operator transparency;
- oracle and slashing risks are hard to price.

## Slide 3: The Insight

The 500,000 HYPE stake is not just a cost.

It is the economic security layer for a market operator.

If HYPE holders fund that stake, they should share in the operator's builder fees.

## Slide 4: Product

HIP.markets is both:

- a HyperEVM HYPE vault;
- a HIP-3 market operator.

Users deposit HYPE. HIP.markets uses it to satisfy the deployer stake requirement. HIP.markets runs markets and distributes net deployer fees to stakers.

## Slide 5: System Flow

1. HYPE holders deposit into vault.
2. Vault backs HIP.markets deployer stake.
3. HIP.markets launches HIP-3 markets.
4. Oracle relayers update prices.
5. Traders generate fees.
6. Net builder fees flow to stakers.

## Slide 6: Why Not Liquid Staking?

Liquid staking earns validator-style yield.

HIP.markets earns operator revenue from markets.

The risks are different:

- oracle risk;
- liquidity risk;
- slashing risk;
- market selection risk;
- fee-revenue risk.

## Slide 7: MVP

Start narrow:

- one HIP.markets-operated DEX;
- one HYPE vault;
- first three tickers;
- conservative caps;
- weekly fee distributions;
- public oracle and risk dashboard.

## Slide 8: Economics

Staker APR depends on:

- daily trading volume;
- effective fee rate;
- deployer share;
- operating costs;
- protocol fee;
- reserve contribution;
- HYPE price.

Base model:

- 500,000 HYPE staked;
- $50M daily volume;
- 6 bps effective fee;
- 50% deployer share;
- 40% combined operating/protocol/reserve deductions;
- approximately 15% APR.

## Slide 9: Risk Controls

HIP.markets wins by being conservative:

- launch simple markets first;
- use redundant oracle feeds;
- cap open interest;
- publish fee recipient and deployer addresses;
- maintain slashing reserve;
- pause deposits during oracle incidents.

## Slide 10: Market Expansion

Phase 1: crypto majors or other oracle-simple markets.

Phase 2: liquid RWA markets with strong data coverage.

Phase 3: commodities and indices after licensing and roll methodology.

Phase 4: HIP-4 outcome markets if deployment and fee mechanics mature.

## Slide 11: Competitive Position

trade.xyz and HyENA prove HIP-3 operator demand.

HIP.markets adds a different primitive:

community-funded deployer stake plus fee sharing.

It is not a neutral allocator at launch. It is the operator.

## Slide 12: Ask

We are looking for:

- HYPE holders for capped beta;
- market makers for first markets;
- oracle/data partners;
- security reviewers;
- Hyperliquid ecosystem feedback on fee routing and deployer custody.

## Slide 13: Closing

HIP.markets turns HYPE holders into economic backers of new Hyperliquid markets.

The first job is not maximizing APR.

The first job is operating markets safely.
