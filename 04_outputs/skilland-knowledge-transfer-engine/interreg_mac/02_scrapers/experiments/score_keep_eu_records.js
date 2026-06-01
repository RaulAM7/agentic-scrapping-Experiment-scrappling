const config = require("./keep_eu_config");
const { normalizeWhitespace, unique } = require("./keep_eu_lib");

function toLowerText(value) {
  return normalizeWhitespace(value).toLowerCase();
}

function detectGroupMatches(text) {
  const lower = toLowerText(text);
  const matches = {};
  for (const [group, keywords] of Object.entries(config.keywordGroups)) {
    matches[group] = unique(keywords.filter((keyword) => lower.includes(keyword.toLowerCase())));
  }
  return matches;
}

function scoreRecency(row) {
  if (row.programming_period === "2021-2027" && row.status.toLowerCase() === "ongoing") {
    return 5;
  }
  if (row.programming_period === "2021-2027") {
    return 4;
  }
  if (row.programming_period === "2014-2020" && row.status.toLowerCase() === "ongoing") {
    return 3;
  }
  if (row.programming_period === "2014-2020") {
    return 2;
  }
  return 1;
}

function scoreGeo(row) {
  const country = (row.partner_country || row.country || "").toLowerCase();
  const region = (row.partner_region || row.region || "").toLowerCase();
  const programme = (row.programme || "").toLowerCase();

  if (["spain", "portugal", "italy"].includes(country)) {
    return 5;
  }
  if (region.includes("canary") || region.includes("madeira") || region.includes("azores")) {
    return 5;
  }
  if (["cape verde", "mauritania", "senegal", "morocco"].includes(country)) {
    return 4;
  }
  if (programme.includes("atlantic") || programme.includes("mediterranean")) {
    return 3;
  }
  return 2;
}

function scoreTopic(matches) {
  const highGroups = [
    "training",
    "capacity_building",
    "knowledge_transfer",
    "sme_support",
    "entrepreneurship",
    "digital",
  ];
  const highCount = highGroups.filter((group) => matches[group].length > 0).length;
  const strongCombo =
    matches.training.length > 0 &&
    (matches.sme_support.length > 0 ||
      matches.entrepreneurship.length > 0 ||
      matches.knowledge_transfer.length > 0);

  if (strongCombo || highCount >= 3) {
    return 5;
  }
  if (highCount === 2) {
    return 4;
  }
  if (highCount === 1) {
    return 3;
  }
  if (matches.dissemination.length > 0 || matches.exploitation.length > 0) {
    return 2;
  }
  return 1;
}

function scoreTrainingTransfer(row, matches) {
  const outputsPresent = Boolean(row.outputs);
  if (
    outputsPresent &&
    (matches.training.length > 0 ||
      matches.capacity_building.length > 0 ||
      matches.knowledge_transfer.length > 0)
  ) {
    return 5;
  }
  if (
    matches.training.length > 0 ||
    matches.capacity_building.length > 0 ||
    matches.knowledge_transfer.length > 0
  ) {
    return 4;
  }
  if (matches.dissemination.length > 0 || matches.exploitation.length > 0) {
    return 3;
  }
  return 1;
}

function scoreBeneficiaries(matches) {
  const beneficiaries = matches.beneficiaries;
  if (
    beneficiaries.some((value) =>
      ["professionals", "workers", "employees", "companies", "entrepreneurs", "smes"].includes(
        value.toLowerCase()
      )
    )
  ) {
    return 5;
  }
  if (beneficiaries.length >= 2) {
    return 4;
  }
  if (beneficiaries.length === 1) {
    return 3;
  }
  return 1;
}

function scoreEntityType(row) {
  const text = `${row.partner_org_type || ""} ${row.partner_name || ""}`.toLowerCase();
  if (
    /(chamber|commerce|cluster|university|research|technology|technological|innovation agency|development agency|employment|business support|incubator|accelerator)/.test(
      text
    )
  ) {
    return 5;
  }
  if (
    /(public authority|municipality|agency|foundation|association|cooperation|regional public authority|local public authority|national public authority)/.test(
      text
    )
  ) {
    return 4;
  }
  if (/(company|enterprise|private)/.test(text)) {
    return 3;
  }
  return 2;
}

function scoreDataQuality(row) {
  const present = [
    row.project_summary,
    row.outputs,
    row.specific_objective,
    row.start_date,
    row.end_date,
    row.status,
    row.partner_name,
    row.partner_country,
    row.contact_url,
  ].filter(Boolean).length;

  if (present >= 8) {
    return 5;
  }
  if (present >= 6) {
    return 4;
  }
  if (present >= 4) {
    return 3;
  }
  if (present >= 2) {
    return 2;
  }
  return 1;
}

function scoreCommercial(row, matches, entityTypeScore, topicScore) {
  if (
    entityTypeScore >= 4 &&
    (matches.training.length > 0 ||
      matches.sme_support.length > 0 ||
      matches.entrepreneurship.length > 0 ||
      matches.knowledge_transfer.length > 0)
  ) {
    return 5;
  }
  if (entityTypeScore >= 4 || topicScore >= 4) {
    return 4;
  }
  if (topicScore >= 3) {
    return 3;
  }
  return 2;
}

function buildBeneficiaries(matches) {
  return unique(matches.beneficiaries.map((value) => value.toLowerCase())).join(" | ");
}

function buildMatchedKeywords(matches) {
  return unique(
    Object.values(matches)
      .flat()
      .map((value) => value.toLowerCase())
  ).join(" | ");
}

function buildScoreReason(row, matches, scores) {
  const reasons = [];
  reasons.push(`${row.programming_period || "unknown period"} ${row.status || "unknown status"}`.trim());
  if (matches.training.length > 0) {
    reasons.push("training/learning signal");
  }
  if (matches.capacity_building.length > 0) {
    reasons.push("capacity-building signal");
  }
  if (matches.knowledge_transfer.length > 0) {
    reasons.push("knowledge-transfer signal");
  }
  if (matches.sme_support.length > 0 || matches.entrepreneurship.length > 0) {
    reasons.push("business-facing beneficiaries");
  }
  if (row.partner_org_type) {
    reasons.push(row.partner_org_type);
  }
  reasons.push(`geo=${scores.geo_score}`);
  return reasons.join("; ");
}

function buildSuggestedAngle(matches) {
  if (matches.sme_support.length > 0 || matches.entrepreneurship.length > 0) {
    return "Convert project outputs into reusable SME and entrepreneurship training journeys.";
  }
  if (matches.digital.length > 0) {
    return "Package digital skills and transformation outputs into structured beneficiary learning tracks.";
  }
  if (matches.training.length > 0 || matches.capacity_building.length > 0) {
    return "Turn training, workshops and capacity-building assets into scalable learning paths.";
  }
  if (matches.dissemination.length > 0 || matches.exploitation.length > 0) {
    return "Move from dissemination assets to reusable knowledge-transfer products and measurable training.";
  }
  return "Structure project methods, outputs and pilot lessons into reusable training for target beneficiaries.";
}

function scoreRecord(row) {
  const text = [
    row.project_name,
    row.project_summary,
    row.specific_objective,
    row.outputs,
    row.notes,
  ]
    .filter(Boolean)
    .join("\n");
  const matches = detectGroupMatches(text);
  const recencyScore = scoreRecency(row);
  const geoScore = scoreGeo(row);
  const topicScore = scoreTopic(matches);
  const trainingTransferScore = scoreTrainingTransfer(row, matches);
  const beneficiaryScore = scoreBeneficiaries(matches);
  const entityTypeScore = scoreEntityType(row);
  const dataQualityScore = scoreDataQuality(row);
  const commercialRelevanceScore = scoreCommercial(row, matches, entityTypeScore, topicScore);

  const weightedScore =
    recencyScore * 0.15 +
    geoScore * 0.15 +
    topicScore * 0.2 +
    trainingTransferScore * 0.2 +
    beneficiaryScore * 0.1 +
    entityTypeScore * 0.1 +
    dataQualityScore * 0.05 +
    commercialRelevanceScore * 0.05;

  return {
    ...row,
    topic_keywords: buildMatchedKeywords(matches),
    training_signal: matches.training.length > 0 ? "yes" : "no",
    capacity_building_signal: matches.capacity_building.length > 0 ? "yes" : "no",
    knowledge_transfer_signal: matches.knowledge_transfer.length > 0 ? "yes" : "no",
    dissemination_signal: matches.dissemination.length > 0 ? "yes" : "no",
    exploitation_signal: matches.exploitation.length > 0 ? "yes" : "no",
    sme_support_signal: matches.sme_support.length > 0 ? "yes" : "no",
    entrepreneurship_signal: matches.entrepreneurship.length > 0 ? "yes" : "no",
    beneficiaries: buildBeneficiaries(matches),
    recency_score: recencyScore,
    geo_score: geoScore,
    topic_score: topicScore,
    training_transfer_score: trainingTransferScore,
    beneficiary_score: beneficiaryScore,
    entity_type_score: entityTypeScore,
    data_quality_score: dataQualityScore,
    commercial_relevance_score: commercialRelevanceScore,
    score: Number(weightedScore.toFixed(2)),
    score_reason: buildScoreReason(
      row,
      matches,
      {
        geo_score: geoScore,
      }
    ),
    suggested_angle: buildSuggestedAngle(matches),
    next_action: row.contact_url
      ? "Review partner website and project page; validate live outputs and training assets."
      : "Review project page manually; validate live outputs and identify a direct partner contact path.",
  };
}

function scoreRecords(rows) {
  return rows.map(scoreRecord).sort((a, b) => b.score - a.score);
}

module.exports = {
  scoreRecords,
};
