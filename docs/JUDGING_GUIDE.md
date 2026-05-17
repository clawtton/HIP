# Judging Guide

This guide is written for a hackathon judge reviewing HIP.markets quickly.

## 60-Second Thesis

HIP.markets is not a generic staking wrapper. It is a HIP-3 market operator financed by a HyperEVM HYPE vault.

Users deposit HYPE, receive vault shares, and help fund the 500,000 HYPE slashable stake required for HIP.markets to operate its own HIP-3 perpetual DEX. HIP.markets then operates markets, runs oracle infrastructure, manages liquidity/risk, and shares net deployer fees with stakers.

## Why This Is A Real Problem

Hyperliquid is already exchange-scale. The latest research snapshot used in this repo cites roughly $307B of 30-day perp volume, $15.6B of 24-hour perp volume, $13.3B of open interest, and $1.1B of annualized revenue on DefiLlama.

HIP-3 opens those rails to new market operators, but the minimum stake is 500,000 HYPE. At the 2026-05-17 API price check of $42.7015, that is about $21.35M before oracle, data, market-maker, audit, legal, and incident-response costs. That is too large for many strong operators and too inaccessible for most HYPE holders.

The standard operator model also leaves a community-alignment gap: deployer fees accrue to the operator fee recipient, while HYPE holders mostly receive ordinary staking yield, currently referenced around 2.37% APY. HIP.markets makes the community the operator stake base and shares net deployer fees back to the people who funded the stake.

## What To Open First

1. Run the demo:

```bash
npm test
npm run validate
npm run serve
```

2. Open:

```text
http://localhost:4173/app/
```

3. Review the pitch deck:

- [presentation/HIP_MARKETS_DECK.md](../presentation/HIP_MARKETS_DECK.md)
- [presentation/HIP_MARKETS_DECK.pptx](../presentation/HIP_MARKETS_DECK.pptx)

## Demo Walkthrough

1. Start at the operator vault dashboard.
   - Notice this is the product UI, not a landing page.
   - The first screen shows vault capacity, APR, oracle cadence, risk state, market launch rail, deposit ticket, and operator monitor.

2. Review the HIP-3 operator path.
   - Vault deployed.
   - Collect HYPE.
   - Escrow stake.
   - HIP-3 approval.
   - Markets live.

3. Change the economics model.
   - HYPE price.
   - Staked HYPE.
   - Daily volume.
   - Effective fee bps.
   - Builder share.
   - Operating/protocol/reserve deductions.

4. Open the contract panel.
   - Configure vault and HYPE token addresses.
   - Connect wallet.
   - Review the `approve -> deposit -> stake escrow -> operator approval` flow.

5. Open the fee ledger and oracle tabs.
   - Fee history shows how deployer economics become distributions.
   - Oracle updates show cadence/deviation state.

## What Is Real In The Prototype

- Economic model and tests.
- Wallet-aware transaction path for deployed contracts.
- Reference vault and registry contracts.
- Operator lifecycle and risk-state modeling.
- Trade.xyz benchmark calculations.
- Brand system, mascot, deck, and docs.

## What Is Still Simulated

- No live HyperEVM deployment.
- No real HYPE token address configured.
- No live HIP-3 deployer stake submission.
- No production oracle relayer.
- No signed market-maker/data-provider agreements.
- No audit.

## What To Evaluate

- Does the product solve a real HIP-3 capital coordination problem?
- Does it correctly avoid promising passive staking yield?
- Does the UI keep risk beside APR?
- Do the contracts model the actual lifecycle deeply enough for a hackathon prototype?
- Is the Trade.xyz benchmark used honestly as reference evidence rather than guaranteed returns?
- Are remaining trust assumptions clearly disclosed?
