import { calculateVaultEconomics } from "../src/model.js";

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

for (const element of Object.values(elements)) {
  element.addEventListener("input", render);
}

render();

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

  setText("stakeUsd", dollars(result.stakeUsd));
  setText("grossBuilderFees", dollars(result.grossBuilderFees));
  setText("netDailyRewards", dollars(result.netDailyRewards));
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
