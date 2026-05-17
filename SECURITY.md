# Security Policy

HIP.markets is a hackathon prototype and has not been audited.

Do not deploy these contracts with user funds without:

- independent smart-contract audit;
- full Solidity test coverage;
- HyperEVM asset-transfer verification;
- HIP-3 stake-routing verification;
- legal review;
- operational key-management review.

## Reporting Security Issues

For hackathon review, open a private issue or contact the repository owner directly. Do not disclose exploitable issues publicly until they have been reviewed.

## Known Non-Production Assumptions

- The vault uses a reference ERC-20-compatible stake asset.
- HIP-3 stake submission is modeled as a controller/multisig handoff.
- Fee distribution can be operator-triggered.
- Oracle and fee reports are reporter-submitted.
- The demo uses configurable placeholder addresses unless deployed addresses are provided.

See [docs/DEPLOYMENT_AND_SECURITY_PLAN.md](docs/DEPLOYMENT_AND_SECURITY_PLAN.md) for the production hardening checklist.
