# Deployment And Security Plan

HIP.markets is not ready for production deposits. This document defines the path from hackathon prototype to a capped beta.

## Deployment Sequence

1. Confirm asset model.
   - Decide whether the vault accepts native HYPE, wrapped HYPE, or an ERC-20-compatible HYPE representation on HyperEVM.
   - Confirm transfer behavior and decimals.

2. Deploy reference contracts to testnet or a local fork.
   - `HipMarketsVault`
   - `HipMarketsRegistry`

3. Configure roles.
   - Owner: protocol multisig.
   - Operator: fee distribution executor.
   - Risk council: emergency/risk multisig.
   - Oracle reporter: relayer monitoring service.
   - Fee reporter: accounting service.
   - Deployer stake controller: controlled address or module used to submit HIP-3 stake actions.

4. Configure frontend.
   - Vault address.
   - HYPE token address.
   - Target chain ID.
   - Registry address in a future version.

5. Run capped private beta.
   - Low vault cap.
   - No extra ticker auctions.
   - First three markets only.
   - Manual weekly fee distribution.
   - Daily oracle/risk report.

6. Move toward production only after external audit, legal review, and confirmed HyperCore fee/stake routing.

## Required Contract Tests

The current repo includes JavaScript model tests. A production track should add Solidity tests for:

- first deposit share minting;
- later deposit proportional share minting;
- reward index accounting;
- reward claims before and after share transfers;
- withdrawal queue, cancel, and finalize flows;
- withdrawal behavior when stake is escrowed;
- vault cap enforcement;
- phase transitions;
- slash-loss accounting;
- role permissions;
- two-step ownership transfer;
- low-level ERC-20 transfer behavior;
- fee/reserve accounting.

## Security Review Checklist

### Vault

- Share price cannot be manipulated through donation attacks.
- Withdrawals cannot drain escrowed stake.
- Slash losses are allocated consistently across all share holders.
- Rewards cannot be claimed twice.
- Receipt token transfers checkpoint rewards correctly.
- Reentrancy lock covers all token-moving paths.
- Owner/risk-council powers are intentionally limited and disclosed.
- Pauses cannot permanently trap funds without governance process.

### Registry

- Reporter roles cannot overwrite unrelated authority.
- Fee epochs are immutable or corrections are clearly versioned.
- Oracle health cannot be spoofed by unauthorized actors.
- Market status and risk state changes emit sufficient events.

### Operator Controls

- Deployer key custody uses multisig/hardware isolation.
- Oracle updater key is separated from treasury keys.
- Fee recipient is publicly verified.
- Incident runbook includes pause, halt, notify, and postmortem steps.

### Economic Controls

- Operating costs are deducted before APR is marketed.
- Reserve policy is explicit.
- Growth mode and rebates are modeled before yield claims.
- Low-volume periods are disclosed.

## Mainnet Readiness Gates

- Independent smart-contract audit.
- HyperEVM-to-HyperCore stake routing verified.
- Fee recipient routing verified.
- At least two oracle/data providers or a documented failover plan.
- At least two market-maker commitments.
- Legal review for vault shares, derivatives-market financing, and jurisdiction gating.
- Public dashboard with addresses, markets, fee epochs, oracle health, and incidents.
