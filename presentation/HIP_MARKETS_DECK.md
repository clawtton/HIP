# HIP.markets Pitch Deck

## Slide 1: Title

**HIP.markets**

Community-backed HIP-3 markets on Hyperliquid.

Fund the market operator. Share the builder fees.

## Slide 2: The Problem

HIP-3 gives builders the right to run custom perpetual DEXs, but one DEX requires 500,000 HYPE staked.

That stake is not enough by itself:

- builders still need oracle infrastructure;
- market makers still need confidence;
- users need clear fee accounting;
- stakers need to see slashing risk beside APR.

## Slide 3: Product Thesis

HIP.markets is not passive liquid staking.

HIP.markets is the operator.

Users deposit HYPE to back the HIP.markets deployer stake. The HIP.markets team launches markets, runs oracles, manages risk, and shares net deployer fees with stakers.

## Slide 4: Why Trade.xyz Matters

trade.xyz proves that HIP-3 can support serious market operators.

We studied its documented UI patterns:

- dense market rail;
- order ticket with clear execution summary;
- positions panel with audit tabs;
- account and market modes;
- Ghost Mode-style observability;
- explicit user warnings.

## Slide 5: UX Translation

HIP.markets adapts trading-terminal UX to an operator vault:

- market rail becomes first-three-market launch rail;
- order ticket becomes HYPE deposit ticket;
- positions panel becomes vault shares, fee history, oracle updates, market launches;
- Ghost Mode becomes operator monitor;
- execution summary becomes fee and APR accounting.

## Slide 6: Demo Screen 1 - Operator Vault

The first screen is not a landing page.

It is the usable operator console:

- vault capacity;
- projected APR;
- oracle cadence;
- risk state;
- 500,000 HYPE stake requirement.

## Slide 7: Demo Screen 2 - Fee Model

Judges can change the core assumptions:

- HYPE price;
- HYPE staked;
- daily volume;
- effective fee bps;
- builder share;
- operating fee;
- protocol fee;
- reserve contribution.

APR updates instantly.

## Slide 8: Demo Screen 3 - Deposit Ticket

The deposit ticket mirrors a trading order pane:

- amount input;
- deposit/withdraw mode;
- stake value;
- gross builder fees;
- net rewards;
- user-specific estimated rewards;
- slashing warning.

## Slide 9: Demo Screen 4 - Audit Tabs

The bottom panel turns fee sharing into an inspectable ledger:

- vault shares;
- fee history;
- oracle updates;
- market launch readiness.

This is where stakers verify that the operator is behaving.

## Slide 10: Demo Screen 5 - Operator Monitor

The right rail makes risk visible:

- fee recipient;
- oracle updater;
- slashing reserve;
- OI utilization;
- incident runbook.

Yield is never shown without operational risk beside it.

## Slide 11: System Flow

1. HYPE holders deposit into the HyperEVM vault.
2. Vault backs the HIP.markets deployer stake.
3. HIP.markets launches first three HIP-3 markets.
4. Oracle relayers update prices.
5. Traders generate fees.
6. Net deployer fees distribute to stakers.

## Slide 12: Economics

Base model:

- 500,000 HYPE staked;
- $50M daily volume;
- 6 bps effective fee;
- 50% deployer share;
- 40% combined operating, protocol, and reserve deductions;
- approximately 15% net APR.

Sensitivity matters more than headline APR.

## Slide 13: Risk Controls

HIP.markets wins by being conservative:

- start with oracle-simple markets;
- avoid extra ticker auction costs at launch;
- cap open interest;
- publish fee recipient and oracle updater;
- maintain slashing reserve;
- pause deposits during oracle incidents.

## Slide 14: MVP

The MVP is intentionally narrow:

- one HIP.markets-operated DEX;
- one HYPE vault;
- first three markets;
- weekly distributions;
- public dashboard;
- no third-party operator financing.

## Slide 15: Roadmap

V1: prove the operator vault and fee-sharing model.

V2: add more HIP.markets market vaults and automated fee verification.

V3: add risk tranching, secondary vault shares, HIP-4 outcome markets, and possibly third-party operator financing.

## Slide 16: Competitive Position

trade.xyz and HyENA operate markets directly.

HIP.markets also operates markets directly, but adds user-funded HYPE stake and transparent fee sharing.

The wedge is not more markets.

The wedge is turning HYPE holders into economic backers of the market operator.

## Slide 17: Ask

We are looking for:

- HYPE holders for capped beta;
- market makers for first markets;
- oracle and data partners;
- security reviewers;
- Hyperliquid ecosystem feedback on deployer custody and fee routing.

## Slide 18: Closing

HIP.markets turns builder-deployed markets into a community-backed operator business.

The first job is not maximizing APR.

The first job is operating markets safely.
