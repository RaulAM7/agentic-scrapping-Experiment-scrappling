# Next Phase Recommendation - ICP2 Source Discovery

Fecha: 2026-06-12

## Decision recomendada

La recomendacion es `Opcion D - enfoque mixto`:

- Empezar con Canarias V1 en extraccion controlada.
- Separar calidad outbound de volumen.
- No hacer scraping frio general.
- Dejar Espana V2 como escalado planificado, con rondas nacionales y autonomicas.

## Ronda 1 — Canarias alta calidad

Objetivo: primeras tandas cuidadas con encaje claro, buena trazabilidad y posibilidad de `personalizacion_1` segura.

Fuentes:

- ICI asociaciones/colectivos de mujeres e igualdad.
- Tenerife Violeta - entidades comprometidas.
- Tenerife Isla Solidaria - asociaciones.
- Red Anagos.
- EAPN Canarias.
- Plena Inclusion Canarias.
- Coordinadora ONGD Canarias.
- Consejos/directorios insulares de mujeres cuando tengan entidades verificables.

Uso:

- Extraer organizaciones, web, contacto publicado, territorio, actividad y fuente.
- No crear contacto personal si no aparece publicado con nombre y cargo.
- Clasificar `sub_icp` de forma conservadora.
- Marcar `copy_variant = mujeres_steam` solo si hay senal de mujeres/igualdad/STEAM/talento femenino.
- Marcar `copy_variant = inclusion_tech_genero` si el encaje es inclusion, empleo, formacion, migracion, juventud, vulnerabilidad, emprendimiento o impacto social con posible componente de genero.

## Ronda 2 — Canarias volumen

Objetivo: ampliar base canaria con registros y datasets, sin bajar el control de calidad.

Fuentes:

- CSV Asociaciones de Canarias.
- CSV Fundaciones de Canarias.
- Registro Regional de Entidades Colaboradoras en Servicios Sociales.
- Directorios de voluntariado de Tenerife, La Palma y otros cabildos.
- Buscadores/datasets de entidades juridicas del Gobierno de Canarias.

Uso:

- Aplicar filtros por denominacion, finalidad, actividad, isla, municipio y keywords ICP2.
- Separar entidades de mujeres/igualdad de inclusion social general.
- Enriquecer con web oficial antes de proponer contacto outbound.
- Marcar como `organization_only` cuando no haya contacto claro.
- Deduplicar contra Ronda 1.

## Ronda 3 — España nacional alta calidad

Objetivo: abrir Espana V2 con redes nacionales y sectoriales donde el encaje es fuerte.

Fuentes:

- Consejo de Participacion de la Mujer.
- Alianza STEAM por el talento femenino.
- AMIT.
- MujeresTech.
- Women in AI Spain.
- ASEME.
- FEDEPE.
- Federacion de Mujeres Progresistas.
- Fundacion Mujeres.
- Red Acoge.
- Plataforma de ONG de Accion Social.
- EAPN Espana.
- Coordinadora ONGD Espana.
- Fundacion Lealtad.

Uso:

- Crear backlog Espana V2 separado de Canarias.
- Priorizar redes con pagina estable, web, contacto institucional y senal tematica.
- Revisar manualmente datos personales publicados.
- Evitar mezclar entidades nacionales con el dataset Canarias V1.

## Ronda 4 — España nacional alto volumen

Objetivo: volumen nacional para fases posteriores, con filtrado fuerte y enriquecimiento.

Fuentes:

- Registro Nacional de Asociaciones.
- Buscador de fundaciones de competencia estatal.
- AECID - Buscador de ONGD.
- Hacesfalta - Directorio de ONG.
- Plataforma del Tercer Sector.
- Registros autonomicos generales de asociaciones y fundaciones.

Uso:

- No usar para outbound directo sin enriquecimiento.
- Filtrar primero por actividad/territorio/keywords.
- Enriquecer web y contacto en una segunda pasada.
- Mantener `source_confidence` bajo o medio hasta validacion de web oficial.

## Ronda 5 — CCAA / escalado territorial

Objetivo: escalar por comunidad despues de validar Canarias y Espana nacional.

Prioridad inicial:

- Andalucia - IAM asociaciones/federaciones de mujeres.
- Comunitat Valenciana - Directorio de Asociaciones en datos abiertos.
- Euskadi - Emakunde asociaciones de mujeres.
- Castilla-La Mancha - organo de consulta y participacion.
- Comunidad de Madrid - recursos/directorios de mujeres y vulnerabilidad.
- Illes Balears - IBDONA y recursos insulares.
- Aragon - IAM y recursos de mujeres.
- Galicia - Igualdade/Xunta y directorios sociales.
- Cataluna - Taula del Tercer Sector para inclusion social.

Uso:

- Ejecutar comunidad por comunidad.
- No mezclar CCAA entre si en la primera extraccion.
- Priorizar fuentes de mujeres/igualdad antes de registros generales.
- Documentar diferencias de formato y filtros.

## Enriquecimiento

Fuentes utiles para completar o validar:

- BOC/subvenciones ICI.
- Convocatorias y beneficiarias del Instituto de las Mujeres.
- Transparencia ONG.
- Fundacion Lealtad.
- Webs propias de entidades.
- Memorias, paginas de equipo, transparencia y junta directiva.
- Datos.gob.es y portales autonomicos de datos abiertos.

Uso:

- Completar web, email generico, telefono, actividad, territorio y prioridad.
- Confirmar actividad reciente.
- Generar `personalizacion_1` solo cuando la fuente diga explicitamente el foco de la entidad.

## Manual review / descartes

Manual review:

- Fuentes con datos personales publicados.
- Consejos de mujeres y organos consultivos.
- Directorios sin exportacion clara.
- Paginas que mezclan entidades sociales, administraciones y empresas.
- Noticias de adhesiones o subvenciones sin listado estable.

Descartar:

- Fuentes sin URL estable.
- Paginas rotas.
- Fuentes sin entidades o sin trazabilidad.
- Fuentes puramente institucionales sin tejido social objetivo.
- Directorios de mujeres profesionales/culturales sin relacion suficiente con ICP2, salvo uso puntual de enriquecimiento.

## Respuestas operativas

1. Hay fuentes suficientes para empezar extraccion Canarias V1?

Si. Canarias V1 esta listo para una extraccion controlada empezando por fuentes de alta calidad y continuando con volumen/enriquecimiento.

2. Que rondas conviene ejecutar?

Ronda 1 Canarias alta calidad, Ronda 2 Canarias volumen, Ronda 3 Espana nacional alta calidad, Ronda 4 Espana nacional alto volumen y Ronda 5 CCAA/escalado territorial.

3. Que fuentes aportan mayor volumen?

CSV Asociaciones de Canarias, Registro Regional de Entidades Colaboradoras de Servicios Sociales, Registro Nacional de Asociaciones, registros autonomicos, IAM Andalucia, AECID, Hacesfalta, Fundacion Lealtad, Plataforma del Tercer Sector y Coordinadora ONGD Espana.

4. Que fuentes aportan mejor calidad outbound?

ICI, Tenerife Violeta, Red Anagos, EAPN Canarias, Plena Inclusion Canarias, Coordinadora ONGD Canarias, Consejo de Participacion de la Mujer, Alianza STEAM, AMIT, MujeresTech, Women in AI Spain, ASEME, FEDEPE, Federacion de Mujeres Progresistas, Fundacion Mujeres, Red Acoge, EAPN Espana, Plataforma ONG Accion Social y Fundacion Lealtad.

5. Que fuentes nacionales merecen fase Espana V2?

Consejo de Participacion de la Mujer, Alianza STEAM, redes mujeres/STEAM, redes de mujeres empresarias, EAPN Espana, Coordinadora ONGD Espana, Plataforma ONG Accion Social, Red Acoge, Fundacion Lealtad, Hacesfalta, AECID, Registro Nacional de Asociaciones y buscador estatal de fundaciones.

6. Que fuentes autonomicas atacar despues?

Andalucia, Comunitat Valenciana, Euskadi, Castilla-La Mancha, Comunidad de Madrid, Illes Balears, Aragon, Galicia y Cataluna, en ese orden inicial salvo que la siguiente fase encuentre mejor disponibilidad tecnica en otra CCAA.

7. Que fuentes solo sirven para enriquecimiento?

BOC/subvenciones ICI, convocatorias y beneficiarias del Instituto de las Mujeres, Transparencia ONG, datos.gob.es como espejo, webs propias, memorias, paginas de equipo y transparencia.

8. Que fuentes se descartan?

Se descartan para extraccion directa las fuentes sin directorio/listado verificable, noticias aisladas sin pagina estable, paginas institucionales puras sin entidades sociales y directorios no relacionados con mujeres, igualdad, inclusion, empleo, formacion, tecnologia, emprendimiento o impacto social.

## Riesgos y controles

- Riesgo de contactos genericos sin persona: separar organizacion de contacto y marcar `contact_quality`.
- Riesgo de datos desactualizados: validar web oficial y actividad reciente.
- Riesgo legal/uso de datos personales: solo usar datos publicados, con revision humana, cadencia prudente y base legitima revisable.
- Riesgo de mezclar geografias: mantener Canarias V1 separado de Espana V2.
- Riesgo de sobre-inferir genero o tecnologia: no marcar foco mujeres/STEAM/IA si no aparece en la fuente.

## Proximo paso recomendado

Crear una spec nueva para extraccion controlada de Canarias V1, con dos lotes separados:

- Lote A: fuentes de alta calidad outbound.
- Lote B: fuentes de volumen canarias con enriquecimiento posterior.

La salida de esa fase, no de esta, podra producir `organizations_clean.csv` y `contacts_clean.csv` si se aprueba explicitamente.
