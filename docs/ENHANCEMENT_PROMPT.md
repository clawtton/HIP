# HIP.markets Enhancement Prompt

Use this prompt to continue polishing HIP.markets into a hackathon-winning, investor-grade submission.

```text
You are improving the HIP.markets repository for a Hyperliquid / HyperEVM hackathon.

Goal:
Make HIP.markets feel like a professional, polished, credible product that could plausibly become the capital allocation and underwriting layer for HIP-3 builder-deployed markets.

Core product:
HIP.markets is the HIP-3 operator. Users deposit HYPE into a HyperEVM vault. The vault pools enough HYPE to satisfy the 500,000 HYPE slashable stake requirement for HIP.markets' own HIP-3 perpetual DEX. HIP.markets runs markets, oracles, liquidity programs, risk controls, fee accounting, and distributes net deployer fees to vault stakers.

Enhancement requirements:

1. Brand and identity
- Create an original HIP.markets visual identity.
- Include a logo, favicon, and mascot.
- The mascot should be a cat because Hyperliquid culture includes cat motifs such as Hypurr/PURR, but do not copy Hyperliquid's logo, mascot, NFTs, or trademarks.
- Position the cat as a "risk sentinel" for the operator vault: alert, technical, and slightly playful, but not childish.
- Keep the palette terminal-native and premium: dark base, mint/green execution accents, blue data accents, amber risk accents.

2. UI/UX
- Keep the first screen as the actual app, not a marketing landing page.
- Improve the app's professional feel: tighter hierarchy, branded header, better launch lifecycle, clearer wallet/contract path, risk dashboard, and proof cards.
- The UI should make the path obvious:
  user deposits HYPE -> vault mints receipt shares -> vault reaches 500k HYPE -> multisig escrows stake -> risk council records HIP-3 approval -> markets go live -> deployer fees flow back.
- Show which steps are user-controlled and which are operator/multisig-controlled.
- Keep risk near yield at all times.

3. Contracts
- Contracts should be reference-quality scaffolds, not toys.
- Vault should include receipt shares, withdrawal queue, vault cap, reward accounting, phase machine, slashing accounting, and role separation.
- Registry should include operator status, launch checklist, oracle health, fee epochs, market status, and risk state.
- Make remaining trust assumptions explicit.

4. Documentation
- README should look strong on GitHub: brand hero, screenshots, product thesis, demo instructions, architecture, contracts, assumptions, and validation.
- Add or update docs for brand system, polish audit, architecture, and hackathon submission.
- Be precise that the current prototype is not audited and not production-ready.

5. Presentation
- Update the presentation deck with:
  - brand/mascot identity;
  - Trade.xyz benchmark economics;
  - screenshots of the demo;
  - contract wiring;
  - deeper contract lifecycle;
  - system flow and risk controls.

6. Verification
- Run tests and validation.
- Rebuild the PPTX.
- Refresh screenshots.
- Commit and push all changes to main.
```

## Execution Notes

This repo now includes the first execution of the prompt:

- branded SVG logo, favicon, and cat mascot;
- branded app shell and mascot/risk-sentinel UI;
- wallet-aware contract wiring;
- expanded contracts and registry;
- refreshed README, docs, screenshots, and deck.
