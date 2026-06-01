const fs = require("fs");
const path = require("path");

const config = require("./keep_eu_wave_config");
const {
  compactText,
  dayStamp,
  escapeRegex,
  fetchBuffer,
  fetchJson,
  fetchText,
  fileExists,
  htmlToText,
  nowIso,
  sleep,
  unique,
  uniqueBy,
  writeBuffer,
  writeCsv,
  writeJson,
  writeText,
} = require("./keep_eu_lib");

const RAW_HEADERS = [
  "source",
  "source_url",
  "retrieved_at",
  "keep_numeric_id",
  "project_id",
  "project_acronym",
  "project_name",
  "programme",
  "programming_period",
  "status",
  "start_date",
  "end_date",
  "lead_partner_name",
  "lead_partner_country",
  "partner_count",
  "themes",
  "project_summary_excerpt",
  "outputs_excerpt",
];

function buildProjectPayload(programmeObjects) {
  return {
    projects: {
      status: null,
      prizes: false,
      only_projects_with_documents: false,
      project_details: {
        start: [],
        without_start: false,
        end: [],
        without_end: false,
      },
      project_budget: {
        range: [],
        without_budget: false,
      },
      themes: {
        list: [],
        type: "or",
      },
      macro_regional_strategies: [],
      only_infrastructure_financed: false,
    },
    programmes: {
      type: [],
      period: [],
      available: programmeObjects,
    },
    partners: {
      status: [],
      type: [],
      nuts_lead: [],
      nuts_partner: [],
      nuts_search_type: "both",
      selectedAreas: {},
    },
    contribution_2014_2020: {
      specific_objectives: {
        thematic_objectives: [],
        thematic_priorities: [],
      },
      thematic_objectives_eni: [],
    },
    contribution_2021_2027: {
      specific_objectives: [],
      intervention: [],
      common_output_indicators: [],
      common_result_indicators: [],
    },
    search: {
      list: [],
      type: null,
      fields: [],
      rawSearchString: "",
    },
    documents: {
      document_lang: [],
      languages: [],
      types: [],
      name: "",
      search: "",
    },
    project_lang: [],
    project_desc_lang: [],
    languages: [],
    translation_languages: [],
    thematic_objectives_eni: [],
    location: null,
  };
}

async function postProjectSearch(payload, page = 1) {
  const suffix = page > 1 ? `?page=${page}` : "";
  return fetchJson(`${config.baseUrl}/api/search/projects/${suffix}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });
}

async function downloadProjectExport(payload, outputFile) {
  const exportPayload = { ...payload, response_type: "excel" };
  const buffer = await fetchBuffer(`${config.baseUrl}/api/search/projects/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "*/*",
    },
    body: JSON.stringify(exportPayload),
  });
  writeBuffer(outputFile, buffer);
}

function extractByRegex(html, regex) {
  const match = html.match(regex);
  return match ? htmlToText(match[1]) : "";
}

function extractParagraphField(html, label) {
  const regex = new RegExp(
    `<strong[^>]*>\\s*${escapeRegex(label)}\\s*:?\\s*<\\/strong>\\s*([\\s\\S]*?)<\\/p>`,
    "i"
  );
  return extractByRegex(html, regex);
}

function extractLooseField(html, label) {
  const regex = new RegExp(`${escapeRegex(label)}[^<]*<\\/strong>([^]*?)<\\/p>`, "i");
  return extractByRegex(html, regex);
}

function extractSpanField(html, label) {
  const regex = new RegExp(
    `<strong[^>]*>\\s*${escapeRegex(label)}\\s*:?\\s*<\\/strong>\\s*<span[^>]*>([\\s\\S]*?)<\\/span>`,
    "i"
  );
  return extractByRegex(html, regex);
}

function extractCollapsibleField(html, label) {
  const regex = new RegExp(
    `${escapeRegex(label)}\\s*\\(EN\\):\\s*<\\/span>\\s*<div class="collapsible-content collapsed">([\\s\\S]*?)<\\/div><a href="#" class="more">`,
    "i"
  );
  return extractByRegex(html, regex);
}

function extractHrefList(html, pattern) {
  const matches = [];
  const regex = new RegExp(`href="(${pattern})"`, "gi");
  let match;
  while ((match = regex.exec(html)) !== null) {
    matches.push(match[1].startsWith("http") ? match[1] : `${config.baseUrl}${match[1]}`);
  }
  return unique(matches);
}

function inferCountryFromAddress(address) {
  if (!address) {
    return "";
  }
  const parts = address.split(",").map((part) => part.trim()).filter(Boolean);
  return parts.length ? parts[parts.length - 1] : "";
}

function inferRegionFromAddress(address) {
  if (!address) {
    return "";
  }
  const parts = address.split(",").map((part) => part.trim()).filter(Boolean);
  if (parts.length >= 2) {
    return parts[parts.length - 2];
  }
  return "";
}

function extractBlockValue(html, label) {
  const pattern = new RegExp(
    `<strong[^>]*>\\s*${escapeRegex(label)}\\s*:?\\s*<\\/strong>\\s*([\\s\\S]*?)(?:<\\/p>|<\\/span>|<\\/dd>)`,
    "i"
  );
  return extractByRegex(html, pattern);
}

function extractBlockHref(html, label) {
  const regex = new RegExp(
    `<strong[^>]*>\\s*${escapeRegex(label)}\\s*:?\\s*<\\/strong>\\s*<a[^>]*href="([^"]+)"`,
    "i"
  );
  const match = html.match(regex);
  return match ? match[1] : "";
}

function parsePartnerBlock(blockHtml, role) {
  const partnerName =
    extractBlockValue(blockHtml, role === "lead" ? "Lead Partner" : "Name") ||
    extractByRegex(blockHtml, /<dt class="accordion-head open-item">\s*([\s\S]*?)\s*<\/dt>/i);
  const address =
    extractBlockValue(blockHtml, "Address") || extractBlockValue(blockHtml, "Department address");

  return {
    partner_name: partnerName,
    partner_role: role,
    lead_partner: role === "lead" ? "yes" : "no",
    partner_legal_status: extractBlockValue(blockHtml, "Legal status"),
    partner_org_type: extractBlockValue(blockHtml, "Organisation type"),
    partner_address: address,
    partner_country: inferCountryFromAddress(address),
    partner_region: inferRegionFromAddress(address),
    partner_website: extractBlockHref(blockHtml, "Website"),
    partner_budget: extractBlockValue(blockHtml, "Total budget"),
    partner_programme_cofinancing: extractBlockValue(blockHtml, "Partner’s programme co-financing"),
    partner_pic: extractBlockValue(blockHtml, "PIC (Participant Identification Code)"),
  };
}

function parsePartners(html) {
  const partners = [];
  const leadMatch = html.match(/<div class="lead-partner">([\s\S]*?)<\/div>\s*<dl class="accordion-list">/i);
  if (leadMatch) {
    partners.push(parsePartnerBlock(leadMatch[1], "lead"));
  }

  const regex = /<dd class="accordion-item">([\s\S]*?)<\/dd>/gi;
  let match;
  while ((match = regex.exec(html)) !== null) {
    partners.push(parsePartnerBlock(match[1], "partner"));
  }

  return partners.filter((partner) => partner.partner_name);
}

function parseProjectDetailHtml(projectHit, html) {
  const projectUrl = `${config.baseUrl}/projects/${projectHit.id}/`;
  const projectName =
    extractByRegex(html, /<h1 class="page-title">([\s\S]*?)<\/h1>/i) ||
    projectHit.translations?.en?.name ||
    "";
  const programme =
    extractByRegex(html, /<a class="programme-link"[^>]*>\s*Programme\s*([\s\S]*?)<\/a>/i) ||
    projectHit.programme?.title ||
    "";
  const programmingPeriodMatch = programme.match(/(\d{4}\s*-\s*\d{4})/);
  const description =
    extractCollapsibleField(html, "Description") || projectHit.translations?.en?.description || "";
  const expectedAchievements =
    extractCollapsibleField(html, "Expected Achievements") ||
    projectHit.translations?.en?.expected_achievements ||
    "";
  const actualAchievements =
    extractCollapsibleField(html, "Actual Achievements") ||
    projectHit.translations?.en?.actual_achievements ||
    "";
  const expectedOutputs =
    extractCollapsibleField(html, "Expected outputs") || projectHit.translations?.en?.expected_outputs || "";
  const deliveredOutputs =
    extractCollapsibleField(html, "Delivered outputs") || projectHit.translations?.en?.delivered_outputs || "";
  const projectOutputs = extractSpanField(html, "Project outputs");
  const deliverables = extractSpanField(html, "Deliverables");
  const specificObjective =
    extractByRegex(html, /Priority specific objective:\s*<\/strong>\s*<span>([\s\S]*?)<\/span>/i) || "";
  const documents = extractHrefList(html, '(?:https:\\/\\/keep\\.eu)?\\/api\\/project-attachment\\/[^"]+');
  const partners = parsePartners(html);
  const leadPartner = partners.find((partner) => partner.lead_partner === "yes") || null;

  return {
    keep_numeric_id: projectHit.id,
    source_url: projectUrl,
    project_name: projectName,
    project_acronym: extractParagraphField(html, "Project acronym") || projectHit.acronym || "",
    project_id: extractParagraphField(html, "Project ID") || String(projectHit.id),
    programme,
    programming_period: programmingPeriodMatch ? programmingPeriodMatch[1].replace(/\s+/g, "") : "",
    status: extractParagraphField(html, "Project status") || extractLooseField(html, "Project status"),
    start_date: extractParagraphField(html, "Project start date"),
    end_date: extractParagraphField(html, "Project end date"),
    latest_update: extractByRegex(html, /Date of latest update:\s*([0-9-]+)/i),
    project_summary: description,
    expected_achievements: expectedAchievements,
    actual_achievements: actualAchievements,
    expected_outputs: expectedOutputs,
    delivered_outputs: deliveredOutputs,
    outputs: unique([projectOutputs, deliverables].filter(Boolean)).join(" || "),
    specific_objective: specificObjective,
    project_budget: extractParagraphField(html, "Total budget/expenditure"),
    eu_funding: extractParagraphField(html, "Total EU funding (amount)"),
    documents_url: documents.join(" | "),
    lead_partner_name: leadPartner ? leadPartner.partner_name : "",
    lead_partner_country: leadPartner ? leadPartner.partner_country : "",
    lead_partner_region: leadPartner ? leadPartner.partner_region : "",
    partners,
    themes: (projectHit.themes || []).map((theme) => theme.title).join(" | "),
  };
}

async function fetchProjectDetail(projectHit, stamp, waveSettings) {
  const htmlDir = path.join(config.outputPaths.rawHtmlDir, "projects");
  const filePath = path.join(
    htmlDir,
    `${stamp}_${waveSettings.waveTag}_keep_eu_project_${projectHit.id}.html`
  );

  let html;
  if (fileExists(filePath)) {
    html = fs.readFileSync(filePath, "utf8");
  } else {
    html = await fetchText(`${config.baseUrl}/projects/${projectHit.id}/`);
    writeText(filePath, html);
    if (waveSettings.detailDelayMs > 0) {
      await sleep(waveSettings.detailDelayMs);
    }
  }

  return parseProjectDetailHtml(projectHit, html);
}

function loadHistoricalProjectIds(currentWaveTag) {
  const htmlDir = path.join(config.outputPaths.rawHtmlDir, "projects");
  if (!fs.existsSync(htmlDir)) {
    return new Set();
  }

  const ids = new Set();
  for (const fileName of fs.readdirSync(htmlDir)) {
    if (!fileName.endsWith(".html")) {
      continue;
    }
    if (currentWaveTag && fileName.includes(`_${currentWaveTag}_`)) {
      continue;
    }
    const match = fileName.match(/keep_eu_project_(\d+)\.html$/);
    if (!match) {
      continue;
    }
    ids.add(Number(match[1]));
  }

  return ids;
}

async function mapWithConcurrency(items, concurrency, worker) {
  const results = new Array(items.length);
  let index = 0;

  async function runWorker() {
    while (true) {
      const currentIndex = index++;
      if (currentIndex >= items.length) {
        break;
      }
      results[currentIndex] = await worker(items[currentIndex], currentIndex);
    }
  }

  const workerCount = Math.max(1, Math.min(concurrency, items.length));
  await Promise.all(Array.from({ length: workerCount }, () => runWorker()));
  return results;
}

function projectHitsToRawRows(projectHits, detailsById, retrievedAt) {
  return projectHits.map((projectHit) => {
    const detail = detailsById.get(projectHit.id);
    return {
      source: config.source,
      source_url: detail?.source_url || `${config.baseUrl}/projects/${projectHit.id}/`,
      retrieved_at: retrievedAt,
      keep_numeric_id: projectHit.id,
      project_id: detail?.project_id || String(projectHit.id),
      project_acronym: detail?.project_acronym || projectHit.acronym || "",
      project_name: detail?.project_name || projectHit.translations?.en?.name || "",
      programme: detail?.programme || projectHit.programme?.title || "",
      programming_period: detail?.programming_period || "",
      status: detail?.status || "",
      start_date: detail?.start_date || "",
      end_date: detail?.end_date || "",
      lead_partner_name: detail?.lead_partner_name || "",
      lead_partner_country: detail?.lead_partner_country || "",
      partner_count: detail?.partners?.length || 0,
      themes: detail?.themes || "",
      project_summary_excerpt: compactText(detail?.project_summary || "", 280),
      outputs_excerpt: compactText(detail?.outputs || "", 220),
    };
  });
}

function detailsToPartnerRows(projectHits, detailsById, retrievedAt) {
  const rows = [];
  for (const projectHit of projectHits) {
    const detail = detailsById.get(projectHit.id);
    if (!detail) {
      continue;
    }

    const partnerRows = detail.partners.length
      ? detail.partners
      : [{ partner_name: "", partner_role: "", lead_partner: "no" }];

    for (const partner of partnerRows) {
      rows.push({
        source: config.source,
        source_url: detail.source_url,
        retrieved_at: retrievedAt,
        record_type: "partner_in_project",
        project_id: detail.project_id,
        project_name: detail.project_name,
        project_acronym: detail.project_acronym,
        programme: detail.programme,
        programming_period: detail.programming_period,
        status: detail.status,
        start_date: detail.start_date,
        end_date: detail.end_date,
        country: detail.lead_partner_country || partner.partner_country || "",
        region: detail.lead_partner_region || partner.partner_region || "",
        partner_name: partner.partner_name || "",
        partner_role: partner.partner_role || "",
        lead_partner: partner.lead_partner || "no",
        partner_country: partner.partner_country || "",
        partner_region: partner.partner_region || "",
        topic_keywords: "",
        project_summary: detail.project_summary,
        specific_objective: detail.specific_objective,
        outputs: detail.outputs,
        documents_url: detail.documents_url,
        training_signal: "",
        capacity_building_signal: "",
        knowledge_transfer_signal: "",
        dissemination_signal: "",
        exploitation_signal: "",
        sme_support_signal: "",
        entrepreneurship_signal: "",
        beneficiaries: "",
        languages: detail.project_summary ? "EN" : "",
        contact_name: "",
        contact_role: "",
        contact_email: "",
        contact_url: partner.partner_website || detail.source_url,
        recency_score: "",
        geo_score: "",
        topic_score: "",
        training_transfer_score: "",
        beneficiary_score: "",
        entity_type_score: "",
        data_quality_score: "",
        commercial_relevance_score: "",
        score: "",
        score_reason: "",
        suggested_angle: "",
        next_action: "",
        notes: [
          `keep_numeric_id=${detail.keep_numeric_id}`,
          partner.partner_org_type ? `partner_org_type=${partner.partner_org_type}` : "",
          partner.partner_legal_status ? `partner_legal_status=${partner.partner_legal_status}` : "",
          detail.project_budget ? `project_budget=${detail.project_budget}` : "",
        ]
          .filter(Boolean)
          .join(" | "),
        partner_org_type: partner.partner_org_type || "",
        partner_legal_status: partner.partner_legal_status || "",
      });
    }
  }

  return rows;
}

async function collectProjectHits(discovery, retrievedAt, waveSettings) {
  const stamp = dayStamp();
  const programmeById = new Map(
    (discovery.filters.programmes.available || []).map((programme) => [programme.id, programme])
  );
  const selectedHits = [];
  const groupSummaries = [];
  const historicalProjectIds = loadHistoricalProjectIds(waveSettings.waveTag);
  const waveSeenIds = new Set(historicalProjectIds);

  for (const group of waveSettings.selectedGroups) {
    const programmeObjects = group.programmeIds.map((id) => programmeById.get(id)).filter(Boolean);
    if (!programmeObjects.length) {
      groupSummaries.push({
        key: group.key,
        label: group.label,
        project_limit: group.projectLimit,
        collected_projects: 0,
        pages_fetched: 0,
        total_available_results: 0,
        missing_programmes: group.programmeIds,
      });
      continue;
    }

    const payload = buildProjectPayload(programmeObjects);
    const rawPrefix = `${stamp}_${waveSettings.waveTag}_keep_eu_${group.key}`;

    writeJson(path.join(config.outputPaths.rawApiDir, `${rawPrefix}_payload.json`), payload);
    await downloadProjectExport(
      payload,
      path.join(config.outputPaths.rawExportDir, `${rawPrefix}_projects_export.xlsx`)
    );

    const groupHits = [];
    const groupSeenIds = new Set();
    let page = 1;
    let totalAvailableResults = 0;
    let skippedHistoricalProjects = 0;
    let skippedWaveDuplicates = 0;

    while (groupHits.length < group.projectLimit) {
      const pageData = await postProjectSearch(payload, page);
      totalAvailableResults = pageData.count || totalAvailableResults;

      writeJson(
        path.join(
          config.outputPaths.rawApiDir,
          `${rawPrefix}_projects_page_${String(page).padStart(3, "0")}.json`
        ),
        pageData
      );

      if (!pageData.results || !pageData.results.length) {
        break;
      }

      for (const hit of pageData.results) {
        const hitId = Number(hit.id);
        if (historicalProjectIds.has(hitId)) {
          skippedHistoricalProjects += 1;
          continue;
        }
        if (waveSeenIds.has(hitId) || groupSeenIds.has(hitId)) {
          skippedWaveDuplicates += 1;
          continue;
        }

        groupSeenIds.add(hitId);
        waveSeenIds.add(hitId);
        groupHits.push(hit);

        if (groupHits.length >= group.projectLimit) {
          break;
        }
      }

      if (!pageData.next) {
        break;
      }
      page += 1;
    }

    const limitedHits = groupHits.slice(0, group.projectLimit);
    selectedHits.push(...limitedHits.map((hit) => ({ ...hit, search_group: group.key })));
    groupSummaries.push({
      key: group.key,
      label: group.label,
      project_limit: group.projectLimit,
      collected_projects: limitedHits.length,
      pages_fetched: page,
      total_available_results: totalAvailableResults,
      skipped_historical_projects: skippedHistoricalProjects,
      skipped_wave_duplicates: skippedWaveDuplicates,
      first_project_ids: limitedHits.slice(0, 10).map((hit) => hit.id),
    });
  }

  const uniqueHits = uniqueBy(selectedHits, (hit) => hit.id).slice(0, waveSettings.projectTarget);
  const details = await mapWithConcurrency(
    uniqueHits,
    waveSettings.detailConcurrency,
    (hit) => fetchProjectDetail(hit, stamp, waveSettings)
  );

  const detailsById = new Map(details.map((detail) => [detail.keep_numeric_id, detail]));
  const rawRows = projectHitsToRawRows(uniqueHits, detailsById, retrievedAt);

  writeCsv(
    path.join(config.outputPaths.samplesDir, `${waveSettings.waveTag}_keep_eu_sample_raw.csv`),
    rawRows,
    RAW_HEADERS
  );

  return {
    stamp,
    groupSummaries,
    projectHits: uniqueHits,
    rawRows,
    partnerRows: detailsToPartnerRows(uniqueHits, detailsById, retrievedAt),
  };
}

async function extractKeepEuWave(discovery, waveSettings) {
  const retrievedAt = nowIso();
  return collectProjectHits(discovery, retrievedAt, waveSettings);
}

module.exports = {
  RAW_HEADERS,
  buildProjectPayload,
  extractKeepEuWave,
};
