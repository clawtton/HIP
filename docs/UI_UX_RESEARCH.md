# UI/UX Research Notes

## Reference: trade.xyz

The HIP.markets demo borrows product patterns from trade.xyz's documented trading interface, but adapts them to a vault/operator workflow instead of copying the trading product.

Observed trade.xyz patterns:

- Dense terminal layout with market context always visible.
- Order ticket with side, order type, amount, leverage, and execution summary.
- Positions panel with tabs for balances, positions, open orders, TWAP, trade history, funding history, order history, and account activity.
- Multiple account and market modes across perps, XYZ equity perps, and spot.
- Ghost Mode-style observability, where users can watch onchain wallet activity in near real time.
- Explicit warnings that observed data is informational and delayed.

Sources:

- https://docs.trade.xyz/getting-started/how-to-place-an-order
- https://docs.trade.xyz/getting-started/positions-panel
- https://docs.trade.xyz/getting-started/ghost-mode
- https://docs.trade.xyz/trading/overview

## HIP.markets Adaptation

HIP.markets is not an order-entry trading app in the MVP. It is a vault plus operator console. The UI therefore translates trade.xyz's trading-terminal conventions into a staking/operator workflow:

| trade.xyz pattern | HIP.markets adaptation |
|---|---|
| Market rail | HIP-3 market launch rail |
| Order ticket | HYPE deposit / withdrawal ticket |
| Order summary | Stake value, builder fees, net rewards, user estimated rewards |
| Positions tabs | Vault shares, fee history, oracle updates, market launches |
| Ghost Mode observability | Operator monitor and transparent deployer/oracle addresses |
| Risk warnings | Slashing and oracle-risk warnings |
| Pro terminal density | Judge-friendly operator dashboard |

## UX Principles

1. Keep capital state visible.
   Users should always see how much of the 500,000 HYPE stake is funded.

2. Keep fee assumptions editable.
   APR should never appear magical. Volume, fee rate, deployer share, costs, and reserves must be inspectable.

3. Put risk beside yield.
   Oracle cadence, slashing reserve, OI utilization, and incident runbooks sit next to APR.

4. Use tabs for audit trails.
   Fee history and oracle updates should feel as inspectable as positions or orders in a trading app.

5. Avoid landing-page behavior.
   The first screen is the usable operator vault terminal, not a marketing hero.

## Demo Walkthrough For Judges

1. Review the left market rail to understand the first three HIP.markets markets.
2. Review the top KPIs: vault capacity, APR, oracle cadence, and risk state.
3. Use scenario presets to test Base, Conservative, Growth Mode, and Low Share economics.
4. Change deposit amount to see user-specific reward estimates.
5. Open Fee History to see how builder fees become distributions.
6. Open Oracle Updates to see how HIP.markets monitors its operator risk.
7. Open Market Launches to see what is still required before mainnet.
