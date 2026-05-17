# HIP.markets Pitch Deck

## Slide 1: Title

**HIP.markets**

Community-backed HIP-3 markets on Hyperliquid.

Fund the market operator. Share the builder fees.

## Slide 2: The Problem

HIP-3 gives builders permissionless market deployment, but one DEX requires 500,000 HYPE staked.

That stake is not enough by itself:

- builders still need oracle infrastructure;
- market makers still need confidence;
- users need clear fee accounting;
- stakers need to see slashing risk beside APR.

## Slide 3: Product Thesis

HIP.markets is not passive liquid staking.

HIP.markets is the operator.

Users deposit HYPE to back the HIP.markets deployer stake. The HIP.markets team launches markets, runs oracles, manages risk, and shares net deployer fees with stakers.

## Slide 4: Why Now

Hyperliquid has moved from one exchange into market infrastructure.

HIP-3 lets specialist operators list new perpetual markets while HyperCore still provides the order book, margining, and settlement rails.

The bottleneck shifts from matching-engine infrastructure to capital, oracle operations, and operator credibility.

## Slide 5: Trade.xyz Reference

![Trade.xyz reference calculations](tradexyz-reference.png)

Trade.xyz is the reference proof that HIP-3 can support meaningful market demand:

- 60 listed markets;
- $2.50B 30-day volume;
- $121.98K total 30-day fees;
- $60.99K estimated deployer share before operating costs;
- 3.47% gross implied APR on a 500k HYPE minimum stake.

Use this as profit-potential evidence, not as the base case.

## Slide 6: Successful Market Pattern

Trade.xyz's highest-volume 30-day tickers are not only crypto assets.

The leading markets include synthetic index exposure, commodities, semiconductors, and liquid RWA-style instruments:

- XYZ100 and SP500 at roughly $444M each;
- SILVER and crude oil above $280M each;
- SNDK, MU, NVDA, BRENTOIL, CBRS, INTC, and GOLD as repeat high-interest markets.

HIP.markets should launch only where oracle confidence, liquidity, and narrative demand overlap.

## Slide 7: Revenue Interpretation

Reference economics:

- HIP-3 deployer share is fixed at 50% from the deployer perspective;
- Trade.xyz reports `deployerFeeScale = 1.0`;
- 30-day total fees of $121.98K imply roughly $60.99K deployer revenue;
- annualized gross revenue is roughly $742K before costs;
- minimum stake value is roughly $21.40M at $42.8085 HYPE.

This is a gross underwriting input. It is not distributable profit until oracle, data, market-maker, legal, protocol, reserve, and incident-response costs are deducted.

## Slide 8: UI Benchmark

trade.xyz proves that serious HIP-3 markets need trading-terminal density.

We studied its documented UI patterns:

- dense market rail;
- order ticket with clear execution summary;
- positions panel with audit tabs;
- account and market modes;
- Ghost Mode-style observability;
- explicit user warnings.

## Slide 9: UX Translation

HIP.markets adapts trading-terminal UX to an operator vault:

- market rail becomes first-three-market launch rail;
- order ticket becomes HYPE deposit ticket;
- positions panel becomes vault shares, fee history, oracle updates, market launches;
- Ghost Mode becomes operator monitor;
- execution summary becomes fee and APR accounting.

## Slide 10: Demo Walkthrough

![HIP.markets demo dashboard](demo-dashboard.png)

The first screen is not a landing page.

It is the usable operator console: vault capacity, projected APR, oracle cadence, risk state, market rail, fee model, deposit ticket, and monitoring panel are visible in one workflow.

## Slide 11: Demo - Fee Model

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

## Slide 12: Demo - Deposit Ticket

The deposit ticket mirrors a trading order pane:

- amount input;
- deposit/withdraw mode;
- stake value;
- gross builder fees;
- net rewards;
- user-specific estimated rewards;
- slashing warning.

## Slide 13: Demo - Audit Ledger

![HIP.markets demo fee ledger](demo-fee-ledger-view.png)

The bottom panel turns fee sharing into an inspectable ledger:

- vault shares;
- fee history;
- oracle updates;
- market launch readiness.

This is where stakers verify that the operator is behaving.

## Slide 14: Demo - Contract Wiring

![HIP.markets contract wiring](demo-contract-wiring.png)

The demo now exposes the onchain transaction path:

- user connects wallet;
- user configures deployed vault and HYPE token addresses;
- user approves HYPE and calls `deposit(uint256)`;
- operator multisig calls `escrowStakeToController()`;
- risk council records HIP-3 operator approval and markets-live status.

## Slide 15: Contract Depth

The reference contracts now model more of the actual business:

- `vHIPM` receipt shares;
- funding, stake-ready, stake-escrowed, approved, live, wind-down, and slashed phases;
- stake-controller escrow handoff;
- fee epoch reporting;
- oracle health reporting;
- launch checklist and risk-state registry.

## Slide 16: System Flow

1. HYPE holders deposit into the HyperEVM vault.
2. Vault backs the HIP.markets deployer stake.
3. Operator multisig escrows funded HYPE to the deployer stake controller.
4. Risk council records HIP-3 operator approval.
5. HIP.markets launches the first three HIP-3 markets.
6. Oracle relayers update prices.
7. Traders generate fees.
8. Operating, protocol, and reserve deductions are applied.
9. Net deployer fees distribute to stakers.

## Slide 17: Economics

Base model:

- 500,000 HYPE staked;
- $50M daily volume;
- 6 bps effective fee;
- 50% deployer share;
- 40% combined operating, protocol, and reserve deductions;
- approximately 15% net APR.

Benchmark model:

- Trade.xyz trailing fees imply approximately 3.47% gross APR on the minimum stake;
- the delta between base and benchmark highlights why market selection and volume concentration matter.

## Slide 18: Risk Controls

HIP.markets wins by being conservative:

- start with oracle-simple markets;
- avoid extra ticker auction costs at launch;
- cap open interest;
- publish fee recipient and oracle updater;
- maintain slashing reserve;
- pause deposits during oracle incidents.

## Slide 19: Cost Stack

The 500k HYPE stake is the entry ticket, not the full cost of business.

HIP.markets must budget for:

- oracle relayers and monitoring;
- licensed and institutional data;
- market-maker incentives;
- frontend/API/indexing infrastructure;
- key management and security reviews;
- legal/compliance work;
- reserves for slashing, incidents, and low-volume periods.

## Slide 20: MVP

The MVP is intentionally narrow:

- one HIP.markets-operated DEX;
- one HYPE vault;
- first three markets;
- weekly distributions;
- public dashboard;
- explicit risk disclosure;
- no third-party operator financing.

## Slide 21: Roadmap

V1: prove the operator vault and fee-sharing model.

V2: add more HIP.markets market vaults and automated fee verification.

V3: add risk tranching, secondary vault shares, HIP-4 outcome markets, and possibly third-party operator financing once the trust model is mature.

## Slide 22: Competitive Position

trade.xyz and HyENA operate markets directly.

HIP.markets also operates markets directly, but adds user-funded HYPE stake and transparent fee sharing.

The wedge is not more markets.

The wedge is turning HYPE holders into economic backers of the market operator.

## Slide 23: Ask

We are looking for:

- HYPE holders for capped beta;
- market makers for first markets;
- oracle and data partners;
- security reviewers;
- Hyperliquid ecosystem feedback on deployer custody and fee routing.

## Slide 24: Closing

HIP.markets turns builder-deployed markets into a community-backed operator business.

The first job is not maximizing APR.

The first job is operating markets safely.

## Sources

- Trade[XYZ] analytics snapshot: https://loris.tools/hip3/xyz
- Hyperliquid HIP-3 docs: https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals
- Hyperliquid fees docs: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees
- Supporting calculations: [REFERENCE_CALCULATIONS.md](REFERENCE_CALCULATIONS.md)
