const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");

const outputPaths = {
  rawApiDir: path.join(ROOT, "01_data_sources", "raw_api"),
  rawHtmlDir: path.join(ROOT, "01_data_sources", "raw_html"),
  rawExportDir: path.join(ROOT, "01_data_sources", "raw_exports"),
  samplesDir: path.join(ROOT, "03_samples"),
  processedDir: path.join(ROOT, "04_processed_outputs"),
  reportsDir: path.join(ROOT, "05_reports"),
};

const programmeGroups = [
  {
    key: "mac_2021",
    label: "Interreg MAC 2021-2027",
    programmeIds: [388],
  },
  {
    key: "atlantic_2021",
    label: "Atlantic Area 2021-2027",
    programmeIds: [365],
  },
  {
    key: "next_med_2021",
    label: "NEXT MED 2021-2027",
    programmeIds: [385],
  },
  {
    key: "euro_med_2021",
    label: "EURO MED 2021-2027",
    programmeIds: [377],
  },
  {
    key: "mac_2014",
    label: "Interreg MAC 2014-2020",
    programmeIds: [83],
  },
  {
    key: "atlantic_2014",
    label: "Atlantic Area 2014-2020",
    programmeIds: [59],
  },
  {
    key: "med_2014",
    label: "Mediterranean 2014-2020",
    programmeIds: [55],
  },
];

const defaults = {
  profile: "sample",
  waveTag: "wave1",
  detailConcurrency: 4,
  detailDelayMs: 400,
};

const profiles = {
  sample: {
    projectTarget: 18,
    partnerRowsMin: 100,
    groupLimits: {
      mac_2021: 8,
      atlantic_2021: 8,
      next_med_2021: 5,
      mac_2014: 5,
    },
  },
  broad: {
    projectTarget: 150,
    partnerRowsMin: 500,
    groupLimits: {
      mac_2021: 20,
      atlantic_2021: 40,
      next_med_2021: 40,
      euro_med_2021: 25,
      mac_2014: 15,
      atlantic_2014: 15,
      med_2014: 15,
    },
  },
  deep: {
    projectTarget: 200,
    partnerRowsMin: 1200,
    groupLimits: {
      mac_2021: 20,
      atlantic_2021: 30,
      next_med_2021: 35,
      euro_med_2021: 60,
      mac_2014: 40,
      atlantic_2014: 30,
      med_2014: 60,
    },
  },
};

function buildWaveSettings(overrides = {}) {
  const profileName = overrides.profile || defaults.profile;
  const profile = profiles[profileName];
  if (!profile) {
    throw new Error(`Unknown keep.eu wave profile: ${profileName}`);
  }

  const waveTag = overrides.waveTag || defaults.waveTag;
  const detailConcurrency = Number(overrides.detailConcurrency || defaults.detailConcurrency);
  const detailDelayMs = Number(overrides.detailDelayMs || defaults.detailDelayMs);
  const projectTarget = Number(overrides.projectTarget || profile.projectTarget);
  const partnerRowsMin = Number(overrides.partnerRowsMin || profile.partnerRowsMin);

  const groupLimits = { ...profile.groupLimits, ...(overrides.groupLimits || {}) };
  const selectedGroups = programmeGroups
    .map((group) => ({
      ...group,
      projectLimit: Number(groupLimits[group.key] || 0),
    }))
    .filter((group) => group.projectLimit > 0);

  return {
    profileName,
    waveTag,
    detailConcurrency,
    detailDelayMs,
    projectTarget,
    partnerRowsMin,
    selectedGroups,
  };
}

module.exports = {
  baseUrl: "https://keep.eu",
  source: "keep.eu",
  rootDir: ROOT,
  outputPaths,
  programmeGroups,
  defaults,
  profiles,
  buildWaveSettings,
};
