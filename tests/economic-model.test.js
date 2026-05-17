import assert from "node:assert/strict";
import { calculateVaultEconomics, requiredDailyVolumeForApr } from "../src/model.js";

const base = {
  hypePrice: 42.27,
  stakedHype: 500_000,
  dailyVolume: 50_000_000,
  effectiveFeeBps: 6,
  deployerShare: 0.5,
  operatingFeeShare: 0.2,
  protocolFeeShare: 0.1,
  reserveShare: 0.1
};

const economics = calculateVaultEconomics(base);

assert.equal(Math.round(economics.stakeUsd), 21_135_000);
assert.equal(Math.round(economics.grossTradingFees), 30_000);
assert.equal(Math.round(economics.grossBuilderFees), 15_000);
assert.equal(Math.round(economics.netDailyRewards), 9_000);
assert.ok(economics.apr > 0.15 && economics.apr < 0.16);

const requiredVolume = requiredDailyVolumeForApr({
  ...base,
  targetApr: 0.15
});

assert.ok(requiredVolume > 45_000_000);
assert.ok(requiredVolume < 50_000_000);

assert.throws(() => calculateVaultEconomics({ ...base, deployerShare: 2 }));
assert.throws(() => requiredDailyVolumeForApr({ ...base, effectiveFeeBps: 0 }));

console.log("economic model tests passed");
