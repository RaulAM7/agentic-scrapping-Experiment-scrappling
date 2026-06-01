# Tenerife este/sur/metropolitana

Cobertura completada para los 15 municipios pedidos con un minimo de una fila util por municipio en `tenerife_este.csv`.

## Resumen

- Municipios cubiertos: 15/15
- Filas totales: 15
- Confianza `Alto`: 8
- Confianza `Medio`: 6
- Confianza `Bajo`: 1
- Criterio aplicado: priorizar igualdad; si no habia un canal publicamente util en igualdad, bajar a servicios sociales o bienestar social con fuente municipal oficial.

## Fuentes oficiales usadas

- Arona: pagina oficial de `Servicios Sociales` + `Directorio` municipal.
- Granadilla de Abona: `Grupo de Gobierno` + noticia oficial del 8M / Igualdad.
- La Laguna: pagina oficial del grupo politico municipal de gobierno en `PSOE` + portada del ayuntamiento.
- La Matanza de Acentejo: pagina oficial de `Bienestar Social` + pagina oficial de `Igualdad`.
- La Orotava: `Area de Igualdad` + `Informacion General`.
- La Victoria de Acentejo: `Corporacion y concejalias` + `Area de Bienestar Social`.
- Los Realejos: noticia oficial `Nueva integradora social entre el personal municipal` + pagina oficial de `Servicios Sociales`.
- Los Silos: `Grupo de Gobierno` + portada oficial.
- San Miguel de Abona: `Areas municipales y concejalias` + noticia oficial sobre el equipo descentralizado de valoracion de discapacidad.
- Santa Cruz de Tenerife: pagina oficial de `Atencion Social` + pagina oficial de `Contacto`.
- Santa Ursula: `Grupo de Gobierno` + `Igualdad`.
- Santiago del Teide: `Area de Igualdad` + `Grupo de Gobierno`.
- Tacoronte: `Grupo de Gobierno` + `Servicios Sociales`.
- Tegueste: `Igualdad` + `Servicios Sociales`.
- Vilaflor de Chasna: `Servicios Sociales` + `Corporacion municipal 2023-2027`.

## Dudas y problemas relevantes

- Arona: no localice email publico del area ni correo institucional personal del cargo; queda canal general municipal.
- La Laguna: la delegacion de igualdad queda bien identificada, pero no aparecio correo publico del area ni del concejal en la lectura disponible.
- La Matanza de Acentejo: localice un canal operativo de Bienestar Social, pero no una persona responsable nominal visible en abierto para igualdad/social.
- Los Realejos: se pudo fijar el encaje politico de Macarena Hernandez desde noticia oficial, pero no un canal publico de contacto suficientemente claro; es la fila mas debil del lote.
- San Miguel de Abona: el directorio oficial publica telefono del area, pero no un correo publico especifico de Servicios Sociales.
- Santa Cruz de Tenerife: la web publica telefonos y directorio de oficinas, pero no un email visible ni una persona responsable nominal de acceso rapido para esta tematica.

## Criterio aplicado

- No se inventaron emails ni se dedujeron patrones.
- Cuando existia nombre y cargo oficiales sin correo, se dejo `Unknown` y se mantuvo telefono o canal general.
- Cuando solo aparecia un canal operativo del area, se uso ese correo o telefono y se rebajo la confianza.
- En municipios con fuente politica clara y fuente operativa separada, se combinaron ambas.

## Listo para consolidacion

- El CSV usa exactamente el mismo header que `05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv`.
- Solo se tocaron `tenerife_este.csv` y `tenerife_este.md`.
- Si luego hay una pasada de refinado, priorizar: Los Realejos, La Laguna, La Matanza de Acentejo, Arona y Santa Cruz de Tenerife.
