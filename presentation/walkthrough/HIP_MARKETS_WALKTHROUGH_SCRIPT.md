# HIP.markets Walkthrough Script

## 1. HIP.markets

This is HIP dot markets, a community-backed HIP-3 market operator for Hyperliquid. The simple idea is: HYPE holders fund the operator stake, HIP dot markets operates the markets, and net deployer fees are shared back with the stakers who made those markets possible.

## 2. Why This Matters

Judges should not evaluate this like a cold-start yield app. Hyperliquid already has exchange-scale flow. The current research snapshot shows hundreds of billions in monthly perp volume, more than thirteen billion dollars of open interest, and over a billion dollars of annualized revenue. HIP-3 turns that infrastructure into open market operator infrastructure.

## 3. The 500k HYPE Blocker

The opportunity is blocked by capital. One HIP-3 perpetual DEX requires five hundred thousand HYPE staked on mainnet. At the price check used in this submission, that is roughly twenty one point three five million dollars before oracle operations, data, market maker incentives, audits, legal work, and reserves. Meanwhile current HYPE staking references are around two point three seven percent APY. HIP dot markets creates a separate, higher risk operator-fee product.

## 4. Trade.xyz Proves Demand

Trade dot xyz is the reference case. It proves HIP-3 markets can attract real trading demand across crypto, indexes, commodities, and RWA-style instruments. But in the standard operator model, deployer fees accrue to the operator fee recipient. HIP dot markets changes the incentive design by letting the community fund the stake and share in net deployer economics.

## 5. Core Product

The first product is an operator vault. Users deposit HYPE and receive receipt shares. The vault funds the HIP dot markets deployer stake. The team operates the DEX, launches curated markets, runs oracles, manages liquidity and risk, and distributes net fees after operating costs, protocol fees, and reserve contributions.

## 6. Demo Walkthrough

The demo opens directly into the operator console, not a marketing page. A judge can see the vault capacity, projected APR, market launch rail, deposit ticket, oracle cadence, risk state, and operator monitor in one workflow. The interface borrows trading terminal density from successful HIP-3 products like Trade dot xyz, but translates it into a vault and underwriting experience.

## 7. Fee Model

The calculator is intentionally simple and reviewable. Judges can change HYPE price, staked HYPE, daily volume, fee basis points, deployer share, operating costs, protocol fee, and reserve contribution. The point is not to promise fixed yield. The point is to show exactly which assumptions drive staker returns.

## 8. Contract Wiring

The app also shows the real transaction path. In demo mode it is safe and read-only, but after deployment a user can configure vault and token addresses, connect a wallet, approve HYPE, deposit into the vault, and claim rewards. The remaining operator actions are shown honestly: multisig escrow, HIP-3 approval, and risk-council state changes.

## 9. Reference Contracts

This is not just a front-end mock. The Solidity reference contracts model receipt shares, vault caps, withdrawal queues, rewards, protocol and reserve accounting, slashing losses, operator phase gates, fee epochs, oracle health, market metadata, and risk state. They are not audited, but they show the depth of the production design.

## 10. Why This Should Win

HIP dot markets should score well because it is specific to Hyperliquid, grounded in real HIP-3 mechanics, and commercially realistic. It does not hide risk behind APR. It explains the capital blocker, shows a path for users to participate in operator economics, and gives the ecosystem a new capital allocation layer for builder-deployed markets.

## 11. HIP.markets

The MVP is deliberately focused: one HIP dot markets operated DEX, one HYPE vault, and the first three markets. From there, the product can add automated fee verification, risk tranching, secondary vault shares, and eventually HIP-4 outcome market support. HIP dot markets is the capital allocation and underwriting layer for Hyperliquid builder-deployed markets.
