# First Three Markets Memo

HIP.markets should launch with markets that maximize reliability, not novelty. The first three HIP-3 markets are free from additional ticker auction cost, so they should be used to prove operator discipline: oracle quality, market-maker depth, OI caps, fee accounting, and incident response.

## Selection Criteria

| Criterion | Requirement |
| --- | --- |
| Data quality | Multiple high-quality sources or strong internal/external reference markets |
| Maker support | At least two maker conversations before launch; one signed or publicly disclosed commitment before uncapped trading |
| Manipulation resistance | Deep external liquidity, low single-venue dependency, conservative OI caps |
| Trader demand | Clear Hyperliquid-native trader interest |
| Operational simplicity | No holiday calendar complexity unless the market category requires it |
| Kill criteria | Predefined halt triggers before markets go live |

## Proposed Market 1: `hipm:HYPE`

Rationale:

- Most aligned with the HYPE depositor base.
- Strong narrative loop: HYPE holders fund the operator stake and can trade/monitor the HYPE market.
- Hyperliquid API provides a live HYPE mid reference.

Oracle approach:

- Primary: Hyperliquid internal HYPE mid and liquid external venues where available.
- Secondary: aggregated CEX/DEX spot references where liquidity is sufficient.
- Guardrail: reject updates if deviation exceeds the risk-council threshold or if source quorum drops below minimum.

Initial risk limits:

- Max leverage: 10x.
- Initial max OI: $10M.
- Stale threshold: 9 seconds.
- Deviation watch: 25 bps.
- Red-state deviation: 75 bps or stale updates across two consecutive windows.

Kill criteria:

- Oracle stale for more than 3 update windows.
- Primary and secondary references diverge beyond red-state threshold.
- Maker depth below minimum for 15 minutes.
- Unexpected deployer or oracle-updater key activity.

## Proposed Market 2: `hipm:BTC`

Rationale:

- Deepest crypto reference asset.
- Easiest market to source redundant price data.
- Useful benchmark market for testing fee, liquidity, and OI controls before more exotic listings.

Oracle approach:

- Primary: high-liquidity BTC/USD index from multiple venues.
- Secondary: Hyperliquid BTC mid, major CEX spot/perp references, and institutional index where available.
- Guardrail: volume-weighted source quorum and outlier rejection.

Initial risk limits:

- Max leverage: 15x.
- Initial max OI: $25M.
- Stale threshold: 9 seconds.
- Deviation watch: 15 bps.
- Red-state deviation: 50 bps.

Kill criteria:

- Source quorum below 3 venues.
- BTC external market dislocation that creates unexplained mark/oracle divergence.
- Liquidation clusters caused by oracle update failure.

## Proposed Market 3: `hipm:GOLD`

Rationale:

- Proves HIP.markets can operate beyond crypto while staying in a highly liquid macro asset.
- Strong RWA-style demand pattern seen in existing HIP-3 markets.
- Simpler than single-name equities because the asset has broad institutional price references.

Oracle approach:

- Primary: institutional XAU/USD or gold futures reference, subject to licensing.
- Secondary: PAXG and other liquid tokenized gold references only as a sanity check, not sole source.
- Guardrail: trading-session and holiday logic must be explicit before launch.

Initial risk limits:

- Max leverage: 5x.
- Initial max OI: $5M.
- Stale threshold: 12 seconds during active sessions.
- Deviation watch: 30 bps.
- Red-state deviation: 100 bps.

Kill criteria:

- Missing licensed reference data.
- Holiday/session calendar mismatch.
- PAXG/tokenized-gold reference decouples from institutional gold reference.
- Maker depth below threshold during macro news windows.

## Launch Readiness Checklist

- Stake funded and escrow process rehearsed.
- Fee recipient publicly verified.
- Oracle methodology URI published for all three markets.
- Maker depth target published.
- Risk council halt authority tested.
- Fee epoch report template published.
- Incident postmortem template published.
- Deposits remain capped until two weekly reports are published.

## Why These Three

`hipm:HYPE` tests ecosystem-native alignment. `hipm:BTC` tests reliable high-liquidity crypto operations. `hipm:GOLD` tests the first RWA-style market without jumping directly into equities, holiday-heavy instruments, or licensed index methodology.

