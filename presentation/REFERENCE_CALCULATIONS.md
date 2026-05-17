# Trade.xyz Reference Calculations

Retrieved on 2026-05-17. Use these figures as a dated proof point for profit potential, not as a guaranteed base case for HIP.markets.

## Sources

- Loris Trade[XYZ] analytics page: https://loris.tools/hip3/xyz
- Hyperliquid HIP-3 docs: https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals
- Hyperliquid fees docs: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees
- Hyperliquid API checks on 2026-05-17:
  - `allMids` HYPE price: `$42.8085`
  - `perpDexs` for `xyz`: `deployerFeeScale = 1.0`
  - `delegatorSummary` for Trade.xyz deployer `0x88806a71d74ad0a510b350545c9ae490912f0888`: `739,741.26020752 HYPE` delegated

## Loris Trade[XYZ] Snapshot

- 30-day volume: `$2.50B`
- Listed markets: `60`
- Unique traders: `18,382`
- Trades: `865,614`
- Total fees collected: `$121.98K`
- Estimated open interest: `$2.32B` as of 2026-05-16

Top 30-day markets:

| Rank | Symbol | 30d volume |
| ---: | --- | ---: |
| 1 | XYZ100 | $443.91M |
| 2 | SP500 | $443.48M |
| 3 | SILVER | $297.70M |
| 4 | CL | $282.52M |
| 5 | SNDK | $156.64M |
| 6 | MU | $133.54M |
| 7 | NVDA | $120.49M |
| 8 | BRENTOIL | $104.40M |

## Implied Gross Vault APR

Hyperliquid docs state that, from the HIP-3 deployer perspective, fee share is fixed at `50%`. For `xyz`, the API reports `deployerFeeScale = 1.0`, so this deck treats the deployer share as 50% of trading fees.

```text
30d total fees                         = $121,980
Estimated deployer share               = $121,980 x 50% = $60,990
Annualized gross deployer revenue      = $60,990 x 365 / 30 = $742,045
Minimum required stake value           = 500,000 HYPE x $42.8085 = $21,404,250
Trade.xyz actual delegated stake value = 739,741.26020752 HYPE x $42.8085 = $31,666,628

Gross APR on 500k HYPE minimum stake   = $742,045 / $21,404,250 = 3.47%
Gross APR on actual delegated stake    = $742,045 / $31,666,628 = 2.34%
```

These are gross reference values before HIP.markets operating costs, oracle costs, data licensing, market-maker incentives, protocol fees, insurance reserve contributions, legal/compliance expenses, and any downtime or slashing losses.
