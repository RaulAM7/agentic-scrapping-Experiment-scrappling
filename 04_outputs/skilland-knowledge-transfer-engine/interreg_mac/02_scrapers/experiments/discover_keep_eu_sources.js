const path = require("path");

const config = require("./keep_eu_config");
const { dayStamp, fetchJson, writeJson } = require("./keep_eu_lib");

async function discoverSources() {
  const filters = await fetchJson(`${config.baseUrl}/api/available-filters-v2/`);
  const targetIds = new Set(config.programmeGroups.flatMap((group) => group.programmeIds));
  const selectedProgrammes = (filters.programmes.available || []).filter((programme) =>
    targetIds.has(programme.id)
  );
  const summary = {
    retrieved_at: new Date().toISOString(),
    total_programmes_available: (filters.programmes.available || []).length,
    selected_programmes: selectedProgrammes,
    project_statuses: filters.projects.status || [],
    programme_periods: filters.programmes.period || [],
    partner_countries_of_interest: (filters.partners.countries || []).filter((country) =>
      ["Spain", "Portugal", "Italy", "Cape Verde", "Mauritania", "Senegal", "Morocco"].includes(
        country.title
      )
    ),
  };

  return { filters, summary };
}

async function main() {
  const { filters, summary } = await discoverSources();
  const stamp = dayStamp();
  writeJson(path.join(config.outputPaths.rawApiDir, `${stamp}_keep_eu_available_filters.json`), filters);
  writeJson(path.join(config.outputPaths.reportsDir, `${stamp}_keep_eu_discovery_summary.json`), summary);
  console.log(JSON.stringify(summary, null, 2));
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}

module.exports = {
  discoverSources,
};
