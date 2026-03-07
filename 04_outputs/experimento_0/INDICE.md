# Experimento 0 — Evaluacion de Scrapling

Indice de todos los archivos generados en este experimento.

## Documentos principales

| Archivo | Que es |
|---------|--------|
| `guia-visual-experimento.md` | Explicacion visual y no tecnica de todo el experimento |
| `plan-maestro.md` | Plan de 6 fases que se diseno antes de ejecutar |
| `icp-asesoria-fiscal-contable-canarias.md` | Perfil de cliente ideal (ICP) completo |
| `2026-03-07_icp-prospect-ranking_v1.md` | Ranking de 77 prospectos reales con puntuacion |
| `2026-03-07_scrapling-evaluation-report_v1.md` | Evaluacion tecnica final de Scrapling |

## Logs de ejecucion

| Archivo | Que es |
|---------|--------|
| `logs/fase-0_setup-log.md` | Instalacion y configuracion de Scrapling |
| `logs/fase-1_reconocimiento-fuentes.md` | Mapa de fuentes de datos probadas |

## Scripts

| Archivo | Que hace |
|---------|----------|
| `scripts/extract_paginas_amarillas.py` | Extrae despachos de Paginas Amarillas |
| `scripts/extract_colegio_economistas.py` | Extrae colegiados del Colegio de Economistas |
| `scripts/discovery_spider.py` | Araña que visita fichas individuales para enriquecer datos |

## Datos

| Archivo | Registros | Que contiene |
|---------|-----------|-------------|
| `datos/paginas_amarillas_canarias.json` | 137 | Despachos unicos de 6 busquedas en PA |
| `datos/colegio_economistas_lp.json` | 49 | Colegiados del Colegio de Economistas LP |
| `datos/despachos_enriquecidos.json` | 30 | Fichas rastreadas en profundidad por el Spider |
| `datos/icp_scored_prospects.json` | 77 | Prospectos puntuados segun heuristica ICP |
