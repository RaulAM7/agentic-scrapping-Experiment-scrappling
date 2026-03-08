# DECISIONS

Short decision log.

- 2026-03-01: Decision template initialized. Status: pending
- [inferred] 2026-03-07: Evaluation is comparative — this repo evaluates Scrapling; a sibling repo evaluates an unnamed alternative. All documentation should be structured for later cross-comparison.
- [inferred] 2026-03-07: Evaluation is ICP-grounded, not generic. All tests should connect to the Canary Islands professional firms use case.
- [inferred] 2026-03-07: The experiment uses a docs-first workspace (no runtime/framework defined in STACK.md yet). Python will likely be needed once Scrapling is installed.
- [inferred] 2026-03-07: The Yanira Leyva client case and the Zack Shapiro article serve as reference material for understanding the ICP pain and the AI-native professional firm vision, not as direct inputs to the scraping evaluation.
- 2026-03-07: Beachhead ICP definido: asesorías fiscales/contables independientes en Canarias (1-10 personas, 50-300 clientes). Caso Yanira como validación directa. Artefacto en 04_outputs/icp-asesoria-fiscal-contable-canarias.md
- 2026-03-07: Plan maestro del experimento diseñado con 6 fases (0-5). Cada fase produce un entregable antes de avanzar. Scrapling se evalúa con sus tres fetchers, Spiders y MCP server. Plan en 03_specs/now/001_now.md
- 2026-03-07: El Experimento 1 pivota de research util a dataset accionable para emailing. El output objetivo ya no es solo hallazgo ICP, sino registro contactable y trazable.
- 2026-03-07: Scrapling via API Python queda como stack operativo unico para el Experimento 1. CLI y MCP quedan fuera del nucleo por peor rendimiento observado en el Experimento 0.
- 2026-03-07: Los carriles de discovery quedan cerrados a `google_basic`, `google_maps` y `specialized_directory`. Paginas Amarillas pasa a benchmark/control, no a fuente principal de diseño.
- 2026-03-07: La ejecucion del Experimento 1 queda checkpoint-driven: sin feedback sobre query packs no hay discovery; sin aprobacion de shortlist no hay piloto; sin gates superados no hay escalado.
- 2026-03-07: Checkpoint 1 aprobado por el usuario con `mantener los 4`. La Fase 2 se ejecuta sobre los packs `GB-01`, `GB-02`, `GM-01` y `SD-01`.
- 2026-03-07: Shortlist Fase 2. `PASS`: Google organic -> webs propias con email visible; AAFC Despachos Profesionales; Colegio de Gestores de Santa Cruz de Tenerife (localizador + PDF). `WATCH`: Google Maps first-party; Colegio de Gestores de Las Palmas; Colegio de Economistas de Las Palmas. `DROP`: republishers tipo `ccasesoria`, COETE/COTIME como fuentes primarias de leads.
- 2026-03-07: Microvalidacion tecnica con Scrapling sobre las tres fuentes candidatas. `PASS_TECH`: Google Basic -> webs propias con email visible, AAFC -> Despachos Profesionales. `WATCH`: Gestores Tenerife -> Localiza tu GA + PDF, porque el entrypoint carga pero el PDF no quedo demostrado como fuente reutilizable de emails.
- 2026-03-07: Piloto Fase 3 ejecutado con Scrapling sobre `google_basic_seeded_websites` (12 registros) y `AAFC - Despachos Profesionales` (12 registros). Ambas fuentes dieron 100% email real en la muestra.
- 2026-03-07: Resultado del gate de piloto. `AAFC` pasa a `PASS` para escalado controlado (`source_quality_score=93`, viabilidad integra con Scrapling). `google_basic_seeded_websites` queda en `WATCH` (`source_quality_score=82`) porque la extraccion en webs funciona, pero la discovery live en Google devuelve `429 / sorry` y rompe la exigencia de viabilidad integra.
- 2026-03-07: `AAFC` escalado con Scrapling a 70 registros (`source_quality_score=95`, `gate_pass=True`). Queda como carril `specialized_directory` aprobado para emailing.
- 2026-03-07: `google_basic` queda tecnicamente rescatado con Scrapling usando `StealthySession` en modo `home -> search`. La discovery live en Google ya no depende de seeds manuales.
- 2026-03-07: El raw live de `google_basic` no se debe escalar sin curacion. Google mezcla webs propias con directorios, institucional y ruido editorial aunque la query devuelva SERP util.
- 2026-03-07: `google_basic` pasa a `PASS` solo en modo `curated business-only`. El dataset curado queda en 31 registros (`source_quality_score=95`, `gate_pass=True`, `90.3%` email real).
- 2026-03-07: Dataset consolidado Fase 4 listo para emailing: 101 registros finales (`70 AAFC` + `31 google_basic curated`, `0 overlaps` en la consolidacion actual).
- 2026-03-08: Fase 5 cerrada. La comparativa final concluye que Experimento 1 supera a Experimento 0 en accionabilidad para emailing, reduce la dependencia del directorio generalista y valida `google_basic` + `AAFC` como combinacion operativa dentro de Scrapling.
