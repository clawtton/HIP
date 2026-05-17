export function calculateVaultEconomics(input) {
  const hypePrice = positive(input.hypePrice, "hypePrice");
  const stakedHype = positive(input.stakedHype, "stakedHype");
  const dailyVolume = nonNegative(input.dailyVolume, "dailyVolume");
  const effectiveFeeBps = nonNegative(input.effectiveFeeBps, "effectiveFeeBps");
  const deployerShare = bounded(input.deployerShare, "deployerShare");
  const operatingFeeShare = bounded(input.operatingFeeShare ?? 0, "operatingFeeShare");
  const protocolFeeShare = bounded(input.protocolFeeShare ?? 0, "protocolFeeShare");
  const reserveShare = bounded(input.reserveShare ?? 0, "reserveShare");

  const stakeUsd = stakedHype * hypePrice;
  const grossTradingFees = dailyVolume * (effectiveFeeBps / 10_000);
  const grossBuilderFees = grossTradingFees * deployerShare;
  const operatingFee = grossBuilderFees * operatingFeeShare;
  const protocolFee = grossBuilderFees * protocolFeeShare;
  const reserveContribution = grossBuilderFees * reserveShare;
  const netDailyRewards = Math.max(
    0,
    grossBuilderFees - operatingFee - protocolFee - reserveContribution
  );
  const netAnnualRewards = netDailyRewards * 365;
  const apr = stakeUsd === 0 ? 0 : netAnnualRewards / stakeUsd;

  return {
    stakeUsd,
    grossTradingFees,
    grossBuilderFees,
    operatingFee,
    protocolFee,
    reserveContribution,
    netDailyRewards,
    netAnnualRewards,
    apr
  };
}

export function requiredDailyVolumeForApr(input) {
  const hypePrice = positive(input.hypePrice, "hypePrice");
  const stakedHype = positive(input.stakedHype, "stakedHype");
  const targetApr = nonNegative(input.targetApr, "targetApr");
  const effectiveFeeBps = positive(input.effectiveFeeBps, "effectiveFeeBps");
  const deployerShare = positive(input.deployerShare, "deployerShare");
  const operatingFeeShare = bounded(input.operatingFeeShare ?? 0, "operatingFeeShare");
  const protocolFeeShare = bounded(input.protocolFeeShare ?? 0, "protocolFeeShare");
  const reserveShare = bounded(input.reserveShare ?? 0, "reserveShare");
  const netShare = Math.max(0, 1 - operatingFeeShare - protocolFeeShare - reserveShare);

  if (netShare === 0) return Infinity;

  const annualTarget = hypePrice * stakedHype * targetApr;
  const dailyTarget = annualTarget / 365;
  return dailyTarget / ((effectiveFeeBps / 10_000) * deployerShare * netShare);
}

function positive(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) {
    throw new Error(`${name} must be a positive number`);
  }
  return number;
}

function nonNegative(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0) {
    throw new Error(`${name} must be a non-negative number`);
  }
  return number;
}

function bounded(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0 || number > 1) {
    throw new Error(`${name} must be between 0 and 1`);
  }
  return number;
}
