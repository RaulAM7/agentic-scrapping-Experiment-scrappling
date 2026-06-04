# Twenty Import Mapping - SkilLand IA Mujeres

- Date: 2026-06-04
- Assumption: standard Twenty objects are `Companies` and `People`, with the listed campaign fields created as lightweight custom fields if they do not already exist.

## Organizations / Companies

| CSV field | Twenty object | Twenty field | Notes |
|---|---|---|---|
| organization_name | Companies | Name | Required primary company label. |
| organization_type | Companies | Custom field: organization_type | Useful to separate cabildos from ayuntamientos. |
| island | Companies | Custom field: island | Retain island-level routing context. |
| municipality | Companies | City or Custom field: municipality | Use a custom field if the standard city field is already reserved for another purpose. |
| department_area | Companies | Custom field: department_area | Multi-area values are semicolon-separated. |
| website | Companies | Domain / Website | Use the canonical institutional website. |
| email_main | Companies | Primary email | Company-level default channel; often department or institutional email. |
| phone_main | Companies | Primary phone | Retains the best available institutional phone. |
| source_url | Companies | Custom field: source_url | Traceability back to the public source. |
| source_file | Companies | Custom field: source_file | Preserve repo lineage for audits. |
| source_type | Companies | Custom field: source_type | Helps separate official website vs directory provenance. |
| icp_segment | Companies | Custom field: icp_segment | Primary CRM segmentation field for this campaign. |
| notes | Companies | Notes | Keep import notes visible to operators. |
| quality_flags | Companies | Custom field: quality_flags | Semicolon-separated QA flags. |
| needs_manual_review | Companies | Custom field: needs_manual_review | Filter before outreach. |
| duplicate_possible | Companies | Custom field: duplicate_possible | Useful in post-import QA views. |

## Contacts / People

| CSV field | Twenty object | Twenty field | Notes |
|---|---|---|---|
| organization_name | People | Company relation | Match to the imported company by organization name. |
| contact_name | People | Name | `Unknown` values should be reviewed before production outreach. |
| role_title | People | Job title | Preserve the original institutional role. |
| department_area | People | Custom field: department_area | Normalized department tag for campaign routing. |
| email | People | Primary email | One email per row after conservative split/dedupe. |
| email_type | People | Custom field: email_type | Distinguishes personal vs generic channels. |
| phone | People | Primary phone | May contain more than one public number separated by `|`. |
| island | People | Custom field: island | Useful for routing and reporting. |
| municipality | People | City or Custom field: municipality | Use the same convention as Companies. |
| source_url | People | Custom field: source_url | Traceability back to the public source. |
| source_file | People | Custom field: source_file | Preserve repo lineage for audits. |
| source_type | People | Custom field: source_type | Differentiates official site vs directory provenance. |
| icp_segment | People | Custom field: icp_segment | Campaign segmentation field. |
| notes | People | Notes | Keep QA and merge notes visible to operators. |
| quality_flags | People | Custom field: quality_flags | Semicolon-separated QA flags. |
| high_confidence | People | Custom field: high_confidence | Fast filter for priority review/import. |
| generic_email | People | Custom field: generic_email | Useful to isolate routing-heavy contacts. |
| needs_manual_review | People | Custom field: needs_manual_review | Review queue filter. |
| duplicate_possible | People | Custom field: duplicate_possible | Useful in post-import QA views. |

## Campos custom recomendados

- `campaign_name = IA Mujeres 2026`
- `icp_segment`
- `department_area`
- `source_type`
- `source_url`
- `high_confidence`
- `needs_manual_review`
- `generic_email`
