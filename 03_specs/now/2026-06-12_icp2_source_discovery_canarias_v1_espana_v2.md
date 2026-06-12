# Spec activa: ICP2 Source Discovery Canarias V1 + Espana V2

Fecha: 2026-06-12

## Outcome

Crear un mapa evaluado de caladeros, fuentes, listados y directorios para el nuevo ICP2 de SkilLand IA Mujeres:

`ICP2 - Asociaciones / ONG - Mujeres e Inclusion Tech`

La fase debe servir para decidir la siguiente fase de extraccion, sin crear leads finales ni preparar importaciones CRM/GWS.

## Fuente estrategica

Se han usado como fuente de verdad los documentos del repositorio `funnel-and-offer-academy`:

- `2026-06-12_icp2_handoff_to_scraping_and_crm.md`
- `2026-06-12_icp2_prompt_for_scraping_repo.md`
- `2026-06-12_icp2_asociaciones_ong_definition.md`
- `2026-06-12_icp2_copy_variants.md`
- `2026-06-12_icp2_personalization_rules_addendum.md`

## Contexto operativo

- `business_line = SkilLand IA Mujeres`
- `campaign = IA Mujeres 2026`
- `macro_icp = asociaciones_ong_mujeres_inclusion_tech`
- `sub_icp = mujeres_igualdad_steam` usa `copy_variant = mujeres_steam`
- `sub_icp = inclusion_tecnologica_impacto_social` usa `copy_variant = inclusion_tech_genero`

ICP2 es una ampliacion social/comunitaria del mismo funnel IA Mujeres. No crea un funnel separado.

## Entregables

Crear bajo `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/source_discovery/`:

- `README.md`
- `source_discovery_report.md`
- `source_inventory.csv`
- `source_evaluation_matrix.md`
- `next_phase_recommendation.md`

Esta spec activa queda en `03_specs/now/`.

## Alcance

### Canarias V1

Discovery profundo y practico de fuentes canarias explotables en una siguiente fase:

- ICI asociaciones/colectivos de mujeres e igualdad.
- Tenerife Isla Solidaria.
- Tenerife Violeta.
- Red Anagos.
- CSV Asociaciones de Canarias.
- CSV Fundaciones de Canarias.
- Registro de entidades colaboradoras de servicios sociales.
- Coordinadora ONGD Canarias.
- Plena Inclusion Canarias.
- Directorios insulares y voluntariado.
- BOC/subvenciones ICI.
- EAPN Canarias.
- Otras fuentes canarias relevantes encontradas.

### Espana V2

Discovery amplio nacional, sectorial y autonomico para backlog de escalado:

- Registro Nacional de Asociaciones.
- Registros autonomicos de asociaciones.
- Registros y directorios de fundaciones.
- Instituto de las Mujeres.
- Consejo de Participacion de la Mujer.
- Convocatorias y beneficiarias.
- Alianza STEAM por el talento femenino.
- Redes de mujeres empresarias.
- Redes de mujeres STEAM.
- Federaciones de mujeres.
- Plataformas del Tercer Sector.
- EAPN Espana y redes autonomicas.
- Coordinadora ONGD Espana.
- Red Acoge.
- Fundacion Lealtad.
- Hacesfalta.
- Transparencia ONG.
- Directorios autonomicos de asociaciones de mujeres.
- Redes de empleabilidad, inclusion digital, migracion, juventud y vulnerabilidad.

## Fuera de alcance

No crear:

- `organizations_clean.csv`
- `contacts_clean.csv`
- leads finales
- datasets finales para CRM
- importaciones CRM
- workflows
- envios
- GWS
- scraping masivo final de entidades

No inventar:

- emails
- cargos
- nombres
- actividad
- senales de encaje
- foco de mujeres
- programas
- alianzas

No deducir emails por patron.

## Criterios de evaluacion

Cada fuente se evalua por:

- volumen potencial de organizaciones/contactos;
- cobertura territorial;
- filtrado territorial;
- filtrado tematico;
- filtrado por `sub_icp`;
- presencia de personas, cargos, emails, webs, telefonos o formularios;
- posibilidad de generar `personalizacion_1` segura;
- utilidad para clasificar `sub_icp` y `copy_variant`;
- esfuerzo de extraccion;
- cautelas legales o de uso de datos personales publicados;
- valor como fuente primaria, volumen, enriquecimiento, backlog o descarte.

## Aceptacion

- Los cinco entregables existen en `source_discovery/`.
- `source_inventory.csv` contiene una fila por fuente candidata y conserva `source_url` en todas las filas.
- Canarias V1 y Espana V2 estan separados claramente.
- La matriz no usa cortes arbitrarios tipo "Top 5".
- La recomendacion final propone rondas de extraccion y responde a las preguntas de readiness, volumen, calidad outbound, escalado nacional/autonomico, enriquecimiento, manual review y descartes.
- No se crean `organizations_clean.csv` ni `contacts_clean.csv`.
- No se toca CRM, GWS ni otros repositorios.
- Se ejecuta `git diff --check`.
