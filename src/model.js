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

export function calculateOperatorReadiness(input) {
  const requiredStake = positive(input.requiredStake, "requiredStake");
  const fundedHype = nonNegative(input.fundedHype, "fundedHype");
  const oracleReady = Boolean(input.oracleReady);
  const makerReady = Boolean(input.makerReady);
  const feeRecipientVerified = Boolean(input.feeRecipientVerified);
  const emergencyPlanReady = Boolean(input.emergencyPlanReady);

  const fundingProgress = Math.min(1, fundedHype / requiredStake);
  const remainingHype = Math.max(0, requiredStake - fundedHype);
  const checklist = [oracleReady, makerReady, feeRecipientVerified, emergencyPlanReady];
  const checklistReady = checklist.filter(Boolean).length;
  const readinessScore = (fundingProgress * 0.55) + ((checklistReady / checklist.length) * 0.45);

  let phase = "Funding";
  if (fundingProgress >= 1 && checklistReady < checklist.length) phase = "Stake Ready";
  if (fundingProgress >= 1 && checklistReady === checklist.length) phase = "Ready For HIP-3 Stake";

  return {
    fundingProgress,
    remainingHype,
    checklistReady,
    checklistTotal: checklist.length,
    readinessScore,
    phase
  };
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
