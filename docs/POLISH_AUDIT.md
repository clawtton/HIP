# Repo Polish Audit

This document captures the main gaps found in the HIP.markets hackathon repository and the concrete upgrades added after the review.

## Highest-Impact Gaps Found

1. Contracts were too shallow for the real HIP-3 operator lifecycle.
   - The original vault accepted deposits and tracked rewards, but it did not model funding readiness, stake escrow, operator approval, market-live state, wind-down, or slashing lifecycle.
   - The original registry published metadata, but it did not track launch checklist state, fee epochs, operator status, market status, or role-separated reporters.

2. The app was mostly an APR calculator.
   - It showed deposit economics, but it did not show how deposited HYPE becomes part of a 500,000 HYPE slashable operator stake.
   - It did not expose wallet connectivity or transaction intent for `approve`, `deposit`, `claimRewards`, or operator-stake actions.

3. The presentation and README needed a stronger bridge between proof and product.
   - The Trade.xyz benchmark demonstrated profit potential, but the repo landing flow needed to connect that benchmark to the actual vault/operator workflow.
   - Demo screenshots needed to show lifecycle and contract wiring, not only a static dashboard.

4. Production trust assumptions needed to be more explicit.
   - A real launch still depends on verifying HyperEVM-to-HyperCore control, fee-recipient routing, deployer-key custody, oracle operations, and legal structure.

## Upgrades Added

### Contracts

`HipMarketsVault.sol` now includes:

- ERC-20-style vault receipt shares (`vHIPM`);
- proportional share minting and redemption previews;
- vault cap and fixed withdrawal delay;
- operator phase machine:
  - `Funding`;
  - `StakeReady`;
  - `StakeEscrowed`;
  - `OperatorApproved`;
  - `MarketsLive`;
  - `WindDown`;
  - `Slashed`;
- role split between owner, operator, and risk council;
- `escrowStakeToController()` to model sending funded HYPE toward the HIP-3 deployer stake controller;
- risk-council functions to record operator approval, live markets, wind-down, and slash losses;
- reward distribution with protocol-fee and reserve accounting;
- two-step ownership transfer.

`HipMarketsRegistry.sol` now includes:

- operator status and risk state;
- launch checklist for stake submission, operator approval, oracle runbook, maker commitments, fee recipient verification, and emergency plan readiness;
- market status and risk state;
- oracle-health reports with stale thresholds and deviation limits;
- fee epoch reports for volume, gross fees, deployer fees, operating costs, reserve contribution, and distributed rewards;
- separate risk council, oracle reporter, and fee reporter roles.

### App

The demo now includes:

- wallet connection via injected EIP-1193 wallets;
- configurable vault, HYPE token, and chain ID fields;
- local config persistence;
- `approve(HYPE)` plus `deposit(uint256)` transaction path;
- `claimRewards()` transaction path;
- explicit operator lifecycle from vault deployment through HIP-3 approval and markets live;
- transaction map showing which actions are user-initiated and which require multisig/risk-council execution.

The app still runs safely in demo mode when no deployed contracts are configured.

### Model And Tests

The economic model now includes operator-readiness scoring in addition to APR math:

- funding progress;
- remaining HYPE to 500,000;
- readiness checklist completion;
- phase label.

Tests cover both economics and readiness calculations.

## Remaining Production Gaps

- Confirm whether a HyperEVM contract can directly control the HIP-3 deployer stake or whether a controller/multisig must bridge actions through HyperCore APIs.
- Replace placeholder contract addresses with deployed HyperEVM addresses.
- Add a full Solidity test harness with a local ERC-20 mock, share accounting tests, withdrawal queue tests, slash-loss tests, and reward-distribution tests.
- Add deployment scripts and verified constructor parameters.
- Add audited oracle relayer code and runbooks.
- Add fee-recipient reconciliation against Hyperliquid data.
- Add legal gating before accepting real users.
- Add security review for receipt-token transferability, queued withdrawals, reward accounting, and controller custody.
