# Experimento 1 — Email-First con Scrapling

Indice de los archivos principales generados en `experimento_1`.

## Documentos principales

| Archivo | Que es |
|---------|--------|
| `2026-03-07_plan-maestro-experimento-1-scrapling_v1.md` | Plan maestro de la iteracion email-first |
| `2026-03-07_source-map-experimento-1_v1.md` | Mapa de fuentes por carril con shortlist `pass/watch/drop` |
| `2026-03-08_validation-report_experimento-1_v1.md` | Documento de validacion formal de la iteracion |
| `2026-03-08_evaluation-report_experimento-1-vs-experimento-0_v1.md` | Comparativa final contra el Experimento 0 |
| `2026-03-08_guia-visual-experimento-1.md` | Explicacion visual y no tecnica del experimento |
| `2026-03-07_escalado-aafc_experimento-1_v1.md` | Resumen del escalado de `AAFC` |
| `2026-03-07_escalado-google-basic-curated_experimento-1_v1.md` | Resumen del escalado curado de `google_basic` |
| `2026-03-07_dataset-consolidado-experimento-1_v1.md` | Resumen del dataset consolidado final |

## Datasets y scratch relevantes

| Archivo | Registros | Que contiene |
|---------|-----------|-------------|
| `05_scratch/experimento_1/2026-03-07_aafc-scaled-dataset_experimento-1.json` | 70 | Escalado de `AAFC` |
| `05_scratch/experimento_1/2026-03-07_google-basic-scaled-dataset_experimento-1.json` | 47 | Raw live de `google_basic` |
| `05_scratch/experimento_1/2026-03-07_google-basic-curated-dataset_experimento-1.json` | 31 | Dataset curado de `google_basic` |
| `05_scratch/experimento_1/2026-03-07_consolidated-scaled-dataset_experimento-1.json` | 101 | Dataset consolidado final para emailing |

## Scripts principales

| Archivo | Que hace |
|---------|----------|
| `05_scratch/scripts/experimento_1_validate_sources.py` | Microvalidacion tecnica inicial de fuentes |
| `05_scratch/scripts/experimento_1_pilot_extract.py` | Piloto acotado sobre `AAFC` y `google_basic` |
| `05_scratch/scripts/experimento_1_scale_aafc.py` | Escalado de `AAFC` |
| `05_scratch/scripts/experimento_1_google_basic_experiments.py` | Bateria tecnica de rescate de `google_basic` |
| `05_scratch/scripts/experimento_1_scale_google_basic.py` | Discovery live y escalado raw de `google_basic` |
| `05_scratch/scripts/experimento_1_curate_google_basic.py` | Curacion comercial del raw de `google_basic` |
| `05_scratch/scripts/experimento_1_consolidate_scaled.py` | Consolidacion final `AAFC + google_basic curated` |
