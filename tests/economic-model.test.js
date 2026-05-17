import assert from "node:assert/strict";
import {
  calculateOperatorReadiness,
  calculateVaultEconomics,
  requiredDailyVolumeForApr
} from "../src/model.js";

const base = {
  hypePrice: 42.848,
  stakedHype: 500_000,
  dailyVolume: 50_000_000,
  effectiveFeeBps: 6,
  deployerShare: 0.5,
  operatingFeeShare: 0.2,
  protocolFeeShare: 0.1,
  reserveShare: 0.1
};

const economics = calculateVaultEconomics(base);

assert.equal(Math.round(economics.stakeUsd), 21_424_000);
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

const readiness = calculateOperatorReadiness({
  requiredStake: 500_000,
  fundedHype: 310_420,
  oracleReady: true,
  makerReady: false,
  feeRecipientVerified: true,
  emergencyPlanReady: true
});

assert.equal(Math.round(readiness.fundingProgress * 100), 62);
assert.equal(readiness.remainingHype, 189_580);
assert.equal(readiness.checklistReady, 3);
assert.equal(readiness.phase, "Funding");

const readyForStake = calculateOperatorReadiness({
  ...readiness,
  requiredStake: 500_000,
  fundedHype: 500_000,
  oracleReady: true,
  makerReady: true,
  feeRecipientVerified: true,
  emergencyPlanReady: true
});

assert.equal(readyForStake.phase, "Ready For HIP-3 Stake");

console.log("economic model tests passed");
