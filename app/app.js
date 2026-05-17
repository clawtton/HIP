import { calculateOperatorReadiness, calculateVaultEconomics } from "../src/model.js";

const DEFAULT_CONTRACTS = {
  vaultAddress: "0x0000000000000000000000000000000000000000",
  stakeTokenAddress: "0x0000000000000000000000000000000000000000",
  targetChainId: "0x3e7"
};

const REQUIRED_STAKE = 500000;
const DEMO_FUNDED_HYPE = 310420;
const APPROVE_SELECTOR = "0x095ea7b3";
const DEPOSIT_SELECTOR = "0xb6b55f25";
const CLAIM_REWARDS_SELECTOR = "0x372500ab";

const presets = {
  base: {
    hypePrice: 42.848,
    stakedHype: 500000,
    dailyVolume: 50000000,
    effectiveFeeBps: 6,
    deployerShare: 50,
    operatingFeeShare: 20,
    protocolFeeShare: 10,
    reserveShare: 10
  },
  conservative: {
    hypePrice: 42.848,
    stakedHype: 500000,
    dailyVolume: 10000000,
    effectiveFeeBps: 4,
    deployerShare: 50,
    operatingFeeShare: 25,
    protocolFeeShare: 10,
    reserveShare: 15
  },
  growth: {
    hypePrice: 42.848,
    stakedHype: 500000,
    dailyVolume: 100000000,
    effectiveFeeBps: 1,
    deployerShare: 50,
    operatingFeeShare: 20,
    protocolFeeShare: 10,
    reserveShare: 10
  },
  lowShare: {
    hypePrice: 42.848,
    stakedHype: 500000,
    dailyVolume: 50000000,
    effectiveFeeBps: 6,
    deployerShare: 10,
    operatingFeeShare: 20,
    protocolFeeShare: 10,
    reserveShare: 10
  }
};

const ids = [
  "hypePrice",
  "stakedHype",
  "dailyVolume",
  "effectiveFeeBps",
  "deployerShare",
  "operatingFeeShare",
  "protocolFeeShare",
  "reserveShare"
];

const elements = Object.fromEntries(ids.map((id) => [id, document.getElementById(id)]));
const depositAmount = document.getElementById("depositAmount");
const connectWalletButton = document.getElementById("connectWallet");
const contractDepositButton = document.getElementById("contractDeposit");
const claimRewardsButton = document.getElementById("claimRewards");
const saveContractConfigButton = document.getElementById("saveContractConfig");
const contractInputs = {
  vaultAddress: document.getElementById("vaultAddress"),
  stakeTokenAddress: document.getElementById("stakeTokenAddress"),
  targetChainId: document.getElementById("targetChainId")
};

let walletAccount = "";

for (const element of [...Object.values(elements), depositAmount]) {
  element.addEventListener("input", render);
}

connectWalletButton.addEventListener("click", connectWallet);
contractDepositButton.addEventListener("click", approveAndDeposit);
claimRewardsButton.addEventListener("click", claimRewards);
saveContractConfigButton.addEventListener("click", saveContractConfig);

for (const input of Object.values(contractInputs)) {
  input.addEventListener("input", updateContractMode);
}

document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-preset]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    applyPreset(button.dataset.preset);
  });
});

document.querySelectorAll("[data-tab]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-tab]").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll("[data-panel]").forEach((panel) => panel.classList.add("hidden"));
    button.classList.add("active");
    document.getElementById(button.dataset.tab).classList.remove("hidden");
  });
});

document.querySelectorAll(".market-row").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".market-row").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

loadContractConfig();
render();

function applyPreset(name) {
  const preset = presets[name];
  for (const [key, value] of Object.entries(preset)) {
    elements[key].value = value;
  }
  render();
}

function render() {
  const input = {
    hypePrice: elements.hypePrice.value,
    stakedHype: elements.stakedHype.value,
    dailyVolume: elements.dailyVolume.value,
    effectiveFeeBps: elements.effectiveFeeBps.value,
    deployerShare: Number(elements.deployerShare.value) / 100,
    operatingFeeShare: Number(elements.operatingFeeShare.value) / 100,
    protocolFeeShare: Number(elements.protocolFeeShare.value) / 100,
    reserveShare: Number(elements.reserveShare.value) / 100
  };

  const result = calculateVaultEconomics(input);
  const userShare = Number(depositAmount.value || 0) / Number(input.stakedHype);
  const readiness = calculateOperatorReadiness({
    requiredStake: REQUIRED_STAKE,
    fundedHype: DEMO_FUNDED_HYPE,
    oracleReady: true,
    makerReady: false,
    feeRecipientVerified: true,
    emergencyPlanReady: true
  });

  setText("stakeUsd", dollars(result.stakeUsd));
  setText("grossBuilderFees", dollars(result.grossBuilderFees));
  setText("netDailyRewards", dollars(result.netDailyRewards));
  setText("userDailyRewards", dollars(result.netDailyRewards * userShare));
  setText("apr", percent(result.apr));
  setText("fundingProgress", percent(readiness.fundingProgress, 0));
  setText("fundedHype", number(DEMO_FUNDED_HYPE));
  setText("operatorPhase", readiness.phase);
  setText("remainingStake", `${number(readiness.remainingHype)} HYPE remaining`);
  updateContractMode();
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function dollars(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value);
}

function percent(value, digits = 1) {
  return new Intl.NumberFormat("en-US", {
    style: "percent",
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(value);
}

function number(value) {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 0
  }).format(value);
}

async function connectWallet() {
  if (!window.ethereum) {
    setTxStatus("No injected wallet found. Install a HyperEVM-compatible wallet to use onchain mode.");
    return;
  }

  const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
  walletAccount = accounts[0] || "";
  setText("walletLabel", walletAccount ? shortAddress(walletAccount) : "Connect Wallet");
  document.getElementById("walletAccount").value = walletAccount || "Not connected";
  await ensureChain();
  setTxStatus(walletAccount ? "Wallet connected. Configure deployed vault/token addresses before sending transactions." : "Wallet connection failed.");
}

async function approveAndDeposit() {
  if (!(await readyForTransactions())) return;

  const amount = parseUnits(depositAmount.value || "0", 18);
  if (amount <= 0n) {
    setTxStatus("Enter a positive HYPE amount before depositing.");
    return;
  }

  const { vaultAddress, stakeTokenAddress } = getContractConfig();
  setTxStatus("Requesting HYPE approval...");
  await sendTransaction(stakeTokenAddress, APPROVE_SELECTOR + encodeAddress(vaultAddress) + encodeUint256(amount));

  setTxStatus("Approval submitted. Requesting vault deposit...");
  await sendTransaction(vaultAddress, DEPOSIT_SELECTOR + encodeUint256(amount));
  setTxStatus("Deposit transaction submitted. The vault would mint vHIPM shares after confirmation.");
}

async function claimRewards() {
  if (!(await readyForTransactions())) return;
  const { vaultAddress } = getContractConfig();
  setTxStatus("Requesting reward claim...");
  await sendTransaction(vaultAddress, CLAIM_REWARDS_SELECTOR);
  setTxStatus("Claim transaction submitted.");
}

async function readyForTransactions() {
  if (!window.ethereum) {
    setTxStatus("No injected wallet found. The demo remains in read-only mode.");
    return false;
  }

  if (!walletAccount) {
    await connectWallet();
  }

  const { vaultAddress, stakeTokenAddress } = getContractConfig();
  if (!isAddress(vaultAddress) || !isAddress(stakeTokenAddress) || isZeroAddress(vaultAddress) || isZeroAddress(stakeTokenAddress)) {
    setTxStatus("Configure deployed vault and HYPE token addresses to enable onchain transactions.");
    return false;
  }

  await ensureChain();
  return Boolean(walletAccount);
}

async function ensureChain() {
  if (!window.ethereum) return;
  const { targetChainId } = getContractConfig();
  const current = await window.ethereum.request({ method: "eth_chainId" });
  if (current.toLowerCase() === targetChainId.toLowerCase()) return;

  try {
    await window.ethereum.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: targetChainId }]
    });
  } catch (error) {
    setTxStatus(`Wallet is on ${current}. Switch to target chain ${targetChainId} before sending transactions.`);
  }
}

async function sendTransaction(to, data) {
  return window.ethereum.request({
    method: "eth_sendTransaction",
    params: [{ from: walletAccount, to, data }]
  });
}

function saveContractConfig() {
  localStorage.setItem("hipMarketsContracts", JSON.stringify(getContractConfig()));
  updateContractMode();
  setTxStatus("Contract config saved locally for this browser.");
}

function loadContractConfig() {
  const saved = JSON.parse(localStorage.getItem("hipMarketsContracts") || "null") || DEFAULT_CONTRACTS;
  for (const [key, input] of Object.entries(contractInputs)) {
    input.value = saved[key] || DEFAULT_CONTRACTS[key];
  }
}

function getContractConfig() {
  return Object.fromEntries(
    Object.entries(contractInputs).map(([key, input]) => [key, input.value.trim()])
  );
}

function updateContractMode() {
  const { vaultAddress, stakeTokenAddress } = getContractConfig();
  const configured = isAddress(vaultAddress) && isAddress(stakeTokenAddress) && !isZeroAddress(vaultAddress) && !isZeroAddress(stakeTokenAddress);
  setText("contractMode", configured ? "Onchain ready" : "Demo addresses");
}

function setTxStatus(message) {
  setText("txStatus", message);
}

function parseUnits(value, decimals) {
  const [whole, rawFraction = ""] = String(value).split(".");
  const fraction = rawFraction.slice(0, decimals).padEnd(decimals, "0");
  return BigInt(whole || "0") * (10n ** BigInt(decimals)) + BigInt(fraction || "0");
}

function encodeUint256(value) {
  return value.toString(16).padStart(64, "0");
}

function encodeAddress(address) {
  return address.toLowerCase().replace(/^0x/, "").padStart(64, "0");
}

function isAddress(address) {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

function isZeroAddress(address) {
  return /^0x0{40}$/i.test(address);
}

function shortAddress(address) {
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}
