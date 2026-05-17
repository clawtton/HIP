# Risk Register

| Risk | Severity | Description | Mitigation |
|---|---:|---|---|
| Slashing | Critical | HIP-3 deployer stake can be slashed for malicious or irregular operation. | Conservative launch, oracle monitoring, reserve fund, capped deposits. |
| Oracle failure | Critical | Bad or stale prices can cause liquidations and slash risk. | Redundant feeds, relayers, alerts, halt runbooks. |
| Fee shortfall | High | Deployer fees may not cover operating costs or expected yield. | Publish break-even volume, no fixed APR, conservative costs. |
| Liquidity failure | High | Market makers may not provide depth during volatility. | Signed market-maker commitments, incentives, OI caps. |
| Key compromise | Critical | Deployer or oracle keys may be abused. | Multisig, hardware custody, key rotation, scoped sub-deployers. |
| Smart contract bug | Critical | Vault accounting or withdrawal logic can fail. | Audit before production, caps, test coverage. |
| Regulatory exposure | Critical | Yield shares and derivatives-market operation may trigger legal regimes. | Counsel review, entity structure, geo restrictions. |
| HYPE price risk | Medium | Stake value and APR denominator fluctuate. | Show APR in HYPE and USD, avoid fixed yield claims. |
| Growth mode impact | Medium | Reduced fees can make APR appear lower than projected. | Dashboard fee-mode disclosure. |
| Data licensing | High | RWA/index data may require commercial licenses. | Start with simple markets, use approved data vendors. |
| Market manipulation | High | Thin markets can be manipulated. | OI caps, lower leverage, market-maker depth checks. |
| Withdrawal mismatch | High | HIP-3 stake constraints may delay withdrawals. | Withdrawal queue and explicit lockup disclosure. |
| Governance capture | Medium | Risk committee could approve bad markets. | Multisig, public reports, staged caps. |
| Reputational risk | Medium | First incident can damage trust. | Slow launch, transparent postmortems. |

## Slashing Loss Policy

The MVP should define loss order before deposits:

1. Slashing reserve absorbs first loss where possible.
2. Remaining loss is socialized across vault shares.
3. HIP.markets team contribution or backstop is optional but should be disclosed.

No user should deposit without seeing the loss policy in the UI.

## Pause Policy

Deposits should pause when:

- oracle updates are stale;
- fee recipient changes unexpectedly;
- market enters red incident state;
- deployer key activity is suspicious;
- legal or data-source risk emerges.

Withdrawals should remain open unless processing them would worsen the incident or conflict with HIP-3 stake constraints.
