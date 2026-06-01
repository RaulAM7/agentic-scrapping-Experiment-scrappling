const path = require("path");

const config = require("./keep_eu_config");
const { discoverSources } = require("./discover_keep_eu_sources");
const { extractWave1Sample } = require("./extract_keep_eu_sample");
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

function buildMarkdownReport(context) {
  const programmeLines = context.groupSummaries
    .map(
      (group) =>
        `- ${group.label}: ${group.collected_projects}/${group.project_limit} proyectos tomados`
    )
    .join("\n");

  const topProgrammes = Object.entries(context.programmeCounts)
    .sort((a, b) => b[1] - a[1])
    .map(([programme, count]) => `- ${programme}: ${count} registros`)
    .join("\n");

  const topCountries = Object.entries(context.partnerCountryCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([country, count]) => `- ${country}: ${count} registros`)
    .join("\n");

  const topScores = context.scoredRows
    .slice(0, 10)
    .map(
      (row) =>
        `- ${row.score} | ${row.partner_name || "Sin partner"} | ${row.project_acronym} | ${row.programme}`
    )
    .join("\n");

  return `# Wave 1 sample report

Fecha: ${context.generatedAt}

## Metodo

- Source discovery con \`/api/available-filters-v2/\`.
- Search API oficial de keep.eu via \`/api/search/projects/\`.
- Export oficial XLSX por grupo via \`response_type=excel\`.
- Descarga de fichas HTML de proyecto para enriquecer fechas, estado, partners, outputs y objetivo especifico.
- Modelo de registro final: \`partner_in_project\`.

## Cobertura de la wave

- Proyectos tomados: ${context.projectCount}
- Registros partner_in_project scored: ${context.partnerRowCount}
- Objetivo minimo de partner rows: ${config.targets.partnerRowsMin}

## Grupos ejecutados

${programmeLines}

## Distribucion por programa

${topProgrammes}

## Distribucion por pais de partner

${topCountries}

## Top scores

${topScores}

## Limitaciones

- keep.eu no expone emails directos de partner en abierto sin login, por eso \`contact_email\` queda vacio.
- No todos los proyectos muestran documentos adjuntos; \`documents_url\` solo se rellena cuando la ficha publica los expone.
- El scoring es heuristico y prioriza senales de training, capacity building, knowledge transfer y business-facing beneficiaries.
`;
}

function buildScrapingReport(context) {
  const rawExports = context.rawExportFiles.map((file) => `- ${file}`).join("\n");
  const rawApiFiles = context.rawApiFiles.map((file) => `- ${file}`).join("\n");
  const rawHtmlCount = context.rawHtmlFiles.length;

  return `# Wave 1 scraping report

Fecha: ${context.generatedAt}

## Fuente y vias usadas

- API interna del frontend: \`https://keep.eu/api/search/projects/\`
- Export oficial XLSX: \`response_type=excel\`
- HTML publico de ficha de proyecto: \`https://keep.eu/projects/{id}/\`

## Rutas de output generadas

### raw_exports

${rawExports}

### raw_api

${rawApiFiles}

### raw_html

- ${rawHtmlCount} fichas de proyecto guardadas en \`01_data_sources/raw_html/projects/\`

## Decisiones de ejecucion

- Priorizacion real: MAC 2021-2027, Atlantic Area 2021-2027, MAC 2014-2020 y NEXT MED 2021-2027.
- Extraccion controlada por cuotas de proyecto por grupo para no sobrerrecoger datos irrelevantes.
- Enriquecimiento por ficha HTML solo para la muestra Wave 1, con delay de ${config.delays.detailMs} ms entre fichas.

## Gaps pendientes

- Afinar payloads de busqueda por keywords si hace falta una Wave 2 mas focalizada.
- Añadir parser de adjuntos/documentos cuando el proyecto publica documentos descargables.
- Enriquecer contactos y webs oficiales fuera de keep.eu en una wave posterior.
`;
}

function buildTopOpportunities(context) {
  const lines = context.scoredRows.slice(0, 15).map((row, index) => {
    return `## ${index + 1}. ${row.partner_name || "Sin partner visible"}

- Score: ${row.score}
- Proyecto: ${row.project_name} (${row.project_acronym})
- Programa: ${row.programme}
- Pais partner: ${row.partner_country || "Unknown"}
- Tipo de entidad: ${row.notes.match(/partner_org_type=([^|]+)/)?.[1]?.trim() || "Unknown"}
- Senales: ${row.topic_keywords || "Sin keyword fuerte"}
- Razon: ${row.score_reason}
- Angulo sugerido: ${row.suggested_angle}
- URL fuente: ${row.source_url}
`;
  });

  return `# Wave 1 top opportunities

${lines.join("\n")}`.trim();
}

function countBy(rows, field) {
  return rows.reduce((accumulator, row) => {
    const key = row[field] || "Unknown";
    accumulator[key] = (accumulator[key] || 0) + 1;
    return accumulator;
  }, {});
}

async function main() {
  const stamp = dayStamp();
  const discovery = await discoverSources();
  writeJson(
    path.join(config.outputPaths.rawApiDir, `${stamp}_keep_eu_available_filters.json`),
    discovery.filters
  );

  const extraction = await extractWave1Sample(discovery);
  const scoredRows = scoreRecords(extraction.partnerRows);

  writeCsv(
    path.join(config.outputPaths.samplesDir, "wave1_keep_eu_sample_scored.csv"),
    scoredRows,
    SCORED_HEADERS
  );
  writeCsv(
    path.join(config.outputPaths.processedDir, "wave1_keep_eu_processed_scored.csv"),
    scoredRows,
    SCORED_HEADERS
  );

  const reportContext = {
    generatedAt: new Date().toISOString(),
    projectCount: extraction.projectHits.length,
    partnerRowCount: scoredRows.length,
    scoredRows,
    groupSummaries: extraction.groupSummaries,
    programmeCounts: countBy(scoredRows, "programme"),
    partnerCountryCounts: countBy(scoredRows, "partner_country"),
    rawExportFiles: config.programmeGroups.map(
      (group) =>
        `01_data_sources/raw_exports/${stamp}_keep_eu_${group.key}_projects_export.xlsx`
    ),
    rawApiFiles: [
      `01_data_sources/raw_api/${stamp}_keep_eu_available_filters.json`,
      ...config.programmeGroups.flatMap((group) => [
        `01_data_sources/raw_api/${stamp}_keep_eu_${group.key}_payload.json`,
        `01_data_sources/raw_api/${stamp}_keep_eu_${group.key}_projects_page_001.json`,
      ]),
    ],
    rawHtmlFiles: extraction.projectHits.map(
      (hit) => `01_data_sources/raw_html/projects/${stamp}_keep_eu_project_${hit.id}.html`
    ),
  };

  writeText(
    path.join(config.outputPaths.samplesDir, "wave1_sample_report.md"),
    buildMarkdownReport(reportContext)
  );
  writeText(
    path.join(config.outputPaths.reportsDir, "wave1_scraping_report.md"),
    buildScrapingReport(reportContext)
  );
  writeText(
    path.join(config.outputPaths.reportsDir, "wave1_top_opportunities.md"),
    buildTopOpportunities(reportContext)
  );

  console.log(
    JSON.stringify(
      {
        projects: extraction.projectHits.length,
        partner_rows: scoredRows.length,
        top_score: scoredRows[0]?.score || null,
        outputs: {
          raw_csv: "03_samples/wave1_keep_eu_sample_raw.csv",
          scored_csv: "03_samples/wave1_keep_eu_sample_scored.csv",
          processed_csv: "04_processed_outputs/wave1_keep_eu_processed_scored.csv",
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
