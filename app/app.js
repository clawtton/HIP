import { calculateVaultEconomics } from "../src/model.js";

const presets = {
  base: {
    hypePrice: 42.27,
    stakedHype: 500000,
    dailyVolume: 50000000,
    effectiveFeeBps: 6,
    deployerShare: 50,
    operatingFeeShare: 20,
    protocolFeeShare: 10,
    reserveShare: 10
  },
  conservative: {
    hypePrice: 42.27,
    stakedHype: 500000,
    dailyVolume: 10000000,
    effectiveFeeBps: 4,
    deployerShare: 50,
    operatingFeeShare: 25,
    protocolFeeShare: 10,
    reserveShare: 15
  },
  growth: {
    hypePrice: 42.27,
    stakedHype: 500000,
    dailyVolume: 100000000,
    effectiveFeeBps: 1,
    deployerShare: 50,
    operatingFeeShare: 20,
    protocolFeeShare: 10,
    reserveShare: 10
  },
  lowShare: {
    hypePrice: 42.27,
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

for (const element of [...Object.values(elements), depositAmount]) {
  element.addEventListener("input", render);
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

  setText("stakeUsd", dollars(result.stakeUsd));
  setText("grossBuilderFees", dollars(result.grossBuilderFees));
  setText("netDailyRewards", dollars(result.netDailyRewards));
  setText("userDailyRewards", dollars(result.netDailyRewards * userShare));
  setText("apr", percent(result.apr));
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

function percent(value) {
  return new Intl.NumberFormat("en-US", {
    style: "percent",
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value);
}
