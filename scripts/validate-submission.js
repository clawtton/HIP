import fs from "node:fs";

const required = [
  "README.md",
  "SECURITY.md",
  "app/index.html",
  "contracts/HipMarketsVault.sol",
  "contracts/HipMarketsRegistry.sol",
  "foundry.toml",
  "docs/BUSINESS_PRODUCT_SPEC.md",
  "docs/ARCHITECTURE.md",
  "docs/BRAND_SYSTEM.md",
  "docs/DEPLOYMENT_AND_SECURITY_PLAN.md",
  "docs/DEPLOYMENT_PROOF_CHECKLIST.md",
  "docs/FIRST_THREE_MARKETS_MEMO.md",
  "docs/HYPERLIQUID_DEMAND_RESEARCH.md",
  "docs/ORACLE_OPERATIONS.md",
  "docs/RISK_REGISTER.md",
  "docs/UI_UX_RESEARCH.md",
  "docs/HACKATHON_SUBMISSION.md",
  "docs/ENHANCEMENT_PROMPT.md",
  "docs/JUDGING_GUIDE.md",
  "docs/JEFF_YAN_REVIEW.md",
  "docs/INVESTOR_CRITICAL_REVIEW_AND_EXECUTION_PLAN.md",
  "docs/MARKET_CONTEXT.md",
  "docs/POLISH_AUDIT.md",
  "app/assets/hip-markets-logo.svg",
  "app/assets/hip-cat.svg",
  "app/assets/favicon.svg",
  "data/deployment-manifest.example.json",
  "data/hyperliquid-demand-snapshot.json",
  "presentation/brand-system.html",
  "presentation/brand-system.png",
  "presentation/market-context.html",
  "presentation/market-context.png",
  "presentation/HIP_MARKETS_DECK.md",
  "presentation/HIP_MARKETS_DECK.pptx",
  "presentation/walkthrough/HIP_MARKETS_WALKTHROUGH.mp4",
  "presentation/walkthrough/HIP_MARKETS_WALKTHROUGH_SCRIPT.md",
  "presentation/walkthrough/YOUTUBE_UPLOAD_COPY.md",
  "presentation/walkthrough/manifest.json",
  "presentation/walkthrough/preview-frame.png",
  "scripts/build-walkthrough-video.py",
  "src/model.js",
  "test/HipMarketsRegistry.t.sol",
  "test/HipMarketsVault.t.sol",
  "tests/economic-model.test.js"
];

const missing = required.filter((file) => !fs.existsSync(file));

if (missing.length) {
  console.error("Missing required files:");
  for (const file of missing) console.error(`- ${file}`);
  process.exit(1);
}

console.log("submission file checklist passed");
