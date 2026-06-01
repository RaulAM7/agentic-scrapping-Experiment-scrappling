const path = require("path");

const config = require("./keep_eu_wave_config");
const { discoverSources } = require("./discover_keep_eu_sources");
const { extractKeepEuWave } = require("./extract_keep_eu_wave");
const { scoreRecords } = require("./score_keep_eu_records");
const { dayStamp, writeCsv, writeJson, writeText } = require("./keep_eu_lib");

const SCORED_HEADERS = [
  "source",
  "source_url",
  "retrieved_at",
  "record_type",
  "project_id",
  "project_name",
  "project_acronym",
  "programme",
  "programming_period",
  "status",
  "start_date",
  "end_date",
  "country",
  "region",
  "partner_name",
  "partner_role",
  "lead_partner",
  "partner_country",
  "partner_region",
  "topic_keywords",
  "project_summary",
  "specific_objective",
  "outputs",
  "documents_url",
  "training_signal",
  "capacity_building_signal",
  "knowledge_transfer_signal",
  "dissemination_signal",
  "exploitation_signal",
  "sme_support_signal",
  "entrepreneurship_signal",
  "beneficiaries",
  "languages",
  "contact_name",
  "contact_role",
  "contact_email",
  "contact_url",
  "recency_score",
  "geo_score",
  "topic_score",
  "training_transfer_score",
  "beneficiary_score",
  "entity_type_score",
  "data_quality_score",
  "commercial_relevance_score",
  "score",
  "score_reason",
  "suggested_angle",
  "next_action",
  "notes",
];

function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) {
      continue;
    }
    const [rawKey, inlineValue] = arg.slice(2).split("=");
    const value = inlineValue !== undefined ? inlineValue : argv[index + 1];
    if (inlineValue === undefined && argv[index + 1] && !argv[index + 1].startsWith("--")) {
      index += 1;
    }
    options[rawKey] = value === undefined ? true : value;
  }
  return options;
}

function countBy(rows, field) {
  return rows.reduce((accumulator, row) => {
    const key = row[field] || "Unknown";
    accumulator[key] = (accumulator[key] || 0) + 1;
    return accumulator;
  }, {});
}

function buildMarkdownReport(context) {
  const programmeLines = context.groupSummaries
    .map(
      (group) =>
        `- ${group.label}: ${group.collected_projects}/${group.project_limit} proyectos tomados; ${group.total_available_results} disponibles; ${group.pages_fetched} paginas`
    )
    .join("\n");

  const topProgrammes = Object.entries(context.programmeCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([programme, count]) => `- ${programme}: ${count} registros`)
    .join("\n");

  const topCountries = Object.entries(context.partnerCountryCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([country, count]) => `- ${country}: ${count} registros`)
    .join("\n");

  const topScores = context.scoredRows
    .slice(0, 15)
    .map(
      (row) =>
        `- ${row.score} | ${row.partner_name || "Sin partner"} | ${row.project_acronym} | ${row.programme}`
    )
    .join("\n");

  return `# ${context.waveTag} sample report

Fecha: ${context.generatedAt}

## Metodo

- Source discovery con \`/api/available-filters-v2/\`.
- Search API oficial de keep.eu via \`/api/search/projects/\`.
- Export oficial XLSX por grupo via \`response_type=excel\`.
- Descarga paralela de fichas HTML de proyecto con concurrencia ${context.waveSettings.detailConcurrency}.
- Modelo de registro final: \`partner_in_project\`.

## Cobertura de la wave

- Proyectos tomados: ${context.projectCount}
- Registros partner_in_project scored: ${context.partnerRowCount}
- Objetivo minimo de partner rows: ${context.waveSettings.partnerRowsMin}
- Perfil ejecutado: ${context.waveSettings.profileName}

## Grupos ejecutados

${programmeLines}

## Distribucion por programa

${topProgrammes}

## Distribucion por pais de partner

${topCountries}

## Top scores

${topScores}

## Limitaciones

- keep.eu no expone emails directos de partner en abierto sin login.
- MAC 2021 sigue apareciendo en filtros pero no devolvio proyectos publicos en esta wave.
- El scoring sigue siendo heuristico y sirve para triage, no como decision final.
`;
}

function buildScrapingReport(context) {
  const rawExports = context.rawExportFiles.map((file) => `- ${file}`).join("\n");
  const rawApiFiles = context.rawApiFiles.map((file) => `- ${file}`).join("\n");

  return `# ${context.waveTag} scraping report

Fecha: ${context.generatedAt}

## Fuente y vias usadas

- API interna del frontend: \`https://keep.eu/api/search/projects/\`
- Export oficial XLSX: \`response_type=excel\`
- HTML publico de ficha de proyecto: \`https://keep.eu/projects/{id}/\`

## Volumen de la wave

- Proyectos: ${context.projectCount}
- Registros partner_in_project: ${context.partnerRowCount}
- Fichas HTML guardadas: ${context.rawHtmlFiles.length}

## Rutas de output generadas

### raw_exports

${rawExports}

### raw_api

${rawApiFiles}

### raw_html

- ${context.rawHtmlFiles.length} fichas de proyecto guardadas en \`01_data_sources/raw_html/projects/\`

## Decisiones de ejecucion

- Priorizacion amplia sobre Atlantic, MAC y MED para subir volumen.
- Se compenso la ausencia publica de MAC 2021 con programas adyacentes de mayor densidad.
- Se uso detalle paralelo con caché local para acelerar sin hacer scraping ciego.
`;
}

function buildTopOpportunities(context) {
  const lines = context.scoredRows.slice(0, 20).map((row, index) => {
    return `## ${index + 1}. ${row.partner_name || "Sin partner visible"}

- Score: ${row.score}
- Proyecto: ${row.project_name} (${row.project_acronym})
- Programa: ${row.programme}
- Pais partner: ${row.partner_country || "Unknown"}
- Senales: ${row.topic_keywords || "Sin keyword fuerte"}
- Razon: ${row.score_reason}
- Angulo sugerido: ${row.suggested_angle}
- URL fuente: ${row.source_url}
`;
  });

  return `# ${context.waveTag} top opportunities

${lines.join("\n")}`.trim();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const waveSettings = config.buildWaveSettings({
    profile: args.profile,
    waveTag: args.wave,
    detailConcurrency: args["detail-concurrency"],
    detailDelayMs: args["detail-delay-ms"],
    projectTarget: args.projects,
    partnerRowsMin: args["partner-rows-min"],
  });

  const stamp = dayStamp();
  const discovery = await discoverSources();
  writeJson(
    path.join(
      config.outputPaths.rawApiDir,
      `${stamp}_${waveSettings.waveTag}_keep_eu_available_filters.json`
    ),
    discovery.filters
  );

  const extraction = await extractKeepEuWave(discovery, waveSettings);
  const scoredRows = scoreRecords(extraction.partnerRows);

  const sampleScoredFile = `${waveSettings.waveTag}_keep_eu_sample_scored.csv`;
  const processedScoredFile = `${waveSettings.waveTag}_keep_eu_processed_scored.csv`;
  const sampleReportFile = `${waveSettings.waveTag}_sample_report.md`;
  const scrapingReportFile = `${waveSettings.waveTag}_scraping_report.md`;
  const topOppsFile = `${waveSettings.waveTag}_top_opportunities.md`;

  writeCsv(path.join(config.outputPaths.samplesDir, sampleScoredFile), scoredRows, SCORED_HEADERS);
  writeCsv(path.join(config.outputPaths.processedDir, processedScoredFile), scoredRows, SCORED_HEADERS);

  const rawApiFiles = [
    `01_data_sources/raw_api/${stamp}_${waveSettings.waveTag}_keep_eu_available_filters.json`,
    ...extraction.groupSummaries.flatMap((group) => {
      const prefix = `${stamp}_${waveSettings.waveTag}_keep_eu_${group.key}`;
      const pageFiles = Array.from({ length: group.pages_fetched || 0 }, (_, index) => {
        const page = String(index + 1).padStart(3, "0");
        return `01_data_sources/raw_api/${prefix}_projects_page_${page}.json`;
      });
      return [
        `01_data_sources/raw_api/${prefix}_payload.json`,
        ...pageFiles,
      ];
    }),
  ];

  const reportContext = {
    waveTag: waveSettings.waveTag,
    waveSettings,
    generatedAt: new Date().toISOString(),
    projectCount: extraction.projectHits.length,
    partnerRowCount: scoredRows.length,
    scoredRows,
    groupSummaries: extraction.groupSummaries,
    programmeCounts: countBy(scoredRows, "programme"),
    partnerCountryCounts: countBy(scoredRows, "partner_country"),
    rawExportFiles: waveSettings.selectedGroups.map((group) => {
      return `01_data_sources/raw_exports/${stamp}_${waveSettings.waveTag}_keep_eu_${group.key}_projects_export.xlsx`;
    }),
    rawApiFiles,
    rawHtmlFiles: extraction.projectHits.map((hit) => {
      return `01_data_sources/raw_html/projects/${stamp}_${waveSettings.waveTag}_keep_eu_project_${hit.id}.html`;
    }),
  };

  writeText(path.join(config.outputPaths.samplesDir, sampleReportFile), buildMarkdownReport(reportContext));
  writeText(path.join(config.outputPaths.reportsDir, scrapingReportFile), buildScrapingReport(reportContext));
  writeText(path.join(config.outputPaths.reportsDir, topOppsFile), buildTopOpportunities(reportContext));

  console.log(
    JSON.stringify(
      {
        wave: waveSettings.waveTag,
        profile: waveSettings.profileName,
        projects: extraction.projectHits.length,
        partner_rows: scoredRows.length,
        top_score: scoredRows[0]?.score || null,
        outputs: {
          raw_csv: `03_samples/${waveSettings.waveTag}_keep_eu_sample_raw.csv`,
          scored_csv: `03_samples/${sampleScoredFile}`,
          processed_csv: `04_processed_outputs/${processedScoredFile}`,
          reports: [
            `03_samples/${sampleReportFile}`,
            `05_reports/${scrapingReportFile}`,
            `05_reports/${topOppsFile}`,
          ],
        },
      },
      null,
      2
    )
  );
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
