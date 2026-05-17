# Deployment Proof Checklist

This checklist makes the next proof step explicit. HIP.markets should not ask users to deposit real HYPE until these fields are either filled with deployed addresses or marked intentionally not applicable.

## Address Manifest

| Component | Address | Required Before Deposits |
| --- | --- | --- |
| HyperEVM chain ID | TBD | Yes |
| HYPE stake asset | TBD | Yes |
| Reward asset | TBD | Yes |
| `HipMarketsVault` | TBD | Yes |
| `HipMarketsRegistry` | TBD | Yes |
| Deployer stake controller | TBD | Yes |
| HIP-3 deployer account | TBD | Yes |
| Fee recipient | TBD | Yes |
| Oracle updater | TBD | Yes |
| Protocol multisig | TBD | Yes |
| Risk council multisig | TBD | Yes |
| Fee reporter | TBD | Before first distribution |
| Oracle reporter | TBD | Before markets live |

## Transaction Proofs

| Proof | Status | Evidence |
| --- | --- | --- |
| Vault deployed | Pending | Deployment transaction hash |
| Registry deployed | Pending | Deployment transaction hash |
| User deposit succeeds | Pending | Testnet or capped beta transaction |
| Receipt shares mint correctly | Pending | Event logs and share balance |
| Withdrawal queue works | Pending | Queue + finalize transaction pair |
| Reward distribution works | Pending | Fee distribution transaction |
| Fee recipient verified | Pending | Signed message or onchain config |
| Stake controller handoff rehearsed | Pending | Controlled test transaction or runbook |
| HIP-3 operator approval recorded | Pending | Registry event and disclosure URI |
| Market live state recorded | Pending | Registry event and dashboard state |

## Launch Gates

No production deposits until:

- Solidity tests pass.
- External review or audit plan is scheduled.
- Legal gating memo is complete.
- First-three-market memo is published.
- Oracle methodology is published.
- Market-maker depth requirements are published.
- Emergency pause and halt runbook is rehearsed.
- Fee-recipient path is verified.
- Slashing loss policy is visible in the app.

## Evidence Standard

Each completed checklist item should link to one of:

- transaction hash;
- signed message;
- deployed address;
- public document URI;
- dashboard screenshot;
- incident simulation report.

