import fs from "node:fs";

const required = [
  "README.md",
  "app/index.html",
  "contracts/HipMarketsVault.sol",
  "contracts/HipMarketsRegistry.sol",
  "docs/BUSINESS_PRODUCT_SPEC.md",
  "docs/ARCHITECTURE.md",
  "docs/BRAND_SYSTEM.md",
  "docs/ORACLE_OPERATIONS.md",
  "docs/RISK_REGISTER.md",
  "docs/UI_UX_RESEARCH.md",
  "docs/HACKATHON_SUBMISSION.md",
  "docs/ENHANCEMENT_PROMPT.md",
  "docs/POLISH_AUDIT.md",
  "app/assets/hip-markets-logo.svg",
  "app/assets/hip-cat.svg",
  "app/assets/favicon.svg",
  "presentation/brand-system.html",
  "presentation/brand-system.png",
  "presentation/HIP_MARKETS_DECK.md",
  "presentation/HIP_MARKETS_DECK.pptx",
  "src/model.js",
  "tests/economic-model.test.js"
];

const missing = required.filter((file) => !fs.existsSync(file));

if (missing.length) {
  console.error("Missing required files:");
  for (const file of missing) console.error(`- ${file}`);
  process.exit(1);
}

console.log("submission file checklist passed");
