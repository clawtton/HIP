# Hackathon Submission

## Project

HIP.markets

## One-Liner

HIP.markets pools HYPE from users to back the HIP.markets team's own HIP-3 builder-deployed perpetual DEX, then shares net deployer fees with stakers.

## Problem

HIP-3 lets builders launch custom perp DEXs on Hyperliquid, but one DEX requires 500,000 HYPE staked. That stake is a major capital bottleneck for a market operator. At the same time, HYPE holders need transparent ways to participate in the growth of builder-deployed markets.

## Solution

HIP.markets creates a HYPE vault on HyperEVM. Deposited HYPE backs the HIP.markets HIP-3 deployer stake. The HIP.markets team operates markets, runs oracle infrastructure, manages risk, earns deployer fees, and distributes net fees to stakers.

## What We Built

- Static demo for the vault and APR model.
- Economic model with tests.
- Reference Solidity vault contract.
- Reference registry contract for market and oracle transparency.
- Business/product spec.
- Architecture, oracle, and risk documentation.
- Pitch deck.

## Technical Stack

- HyperEVM-oriented Solidity contracts.
- Static HTML/CSS/JavaScript frontend.
- Node.js economic model and tests.
- Markdown docs and deck for fast judging.

## Why It Is Different

trade.xyz and HyENA are HIP-3 market operators. HIP.markets is also a market operator, but it adds a community-backed HYPE vault and fee-sharing layer. Users are not passively staking into a generic yield product; they are backing the HIP.markets DEX and receiving a share of its net builder economics.

## MVP Scope

- One DEX.
- One vault.
- First three markets.
- Conservative caps.
- Weekly distributions.
- Public oracle and fee dashboard.

## Demo

Run:

```bash
npm test
npm run validate
npm run serve
```

Open:

```text
http://localhost:4173/app/
```

## What Is Not Done

- No audited contracts.
- No live HyperEVM deployment.
- No production fee-recipient routing.
- No final legal structure.
- No signed market-maker or data-provider agreements.

## Next Steps

1. Verify HyperEVM control path for deployer stake and fee routing.
2. Select first three markets.
3. Secure oracle and market-maker partners.
4. Audit contracts.
5. Launch capped private beta.
6. Publish monthly risk and revenue reports.
