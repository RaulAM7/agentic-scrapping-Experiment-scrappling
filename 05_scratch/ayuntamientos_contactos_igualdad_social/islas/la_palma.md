# La Palma

Cobertura completada para los 14 municipios de La Palma con un mínimo de una fila útil y recomendada por municipio en [la_palma.csv](/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling/05_scratch/ayuntamientos_contactos_igualdad_social/islas/la_palma.csv).

## Resumen

- Municipios cubiertos: 14/14
- Filas totales: 14
- Confianza `Alto`: 8
- Confianza `Medio`: 6
- Prioridad `Alta`: 9
- Prioridad `Media`: 5

## Fuentes usadas

- Barlovento: página oficial de `Servicios Sociales` + noticia institucional reciente que identifica a Janet Díaz.
- Breña Alta: `Corporación local` + `Directorio municipal`.
- Breña Baja: `Grupo de Gobierno` + `Contacto`.
- El Paso: `Concejalías` + `Contacto`.
- Fuencaliente: noticia oficial de reparto de áreas + `Directorio Contactos`.
- Garafía: `Corporación Municipal` + `Servicios Sociales`.
- Los Llanos de Aridane: `Concejalía de Igualdad` + `Equipo de Gobierno`.
- Puntagorda: `Concejalías` + `Servicios Sociales`.
- Puntallana: noticias institucionales del área social/igualdad + página general de `Áreas y Servicios`.
- San Andrés y Sauces: `Dependencias` + páginas de `Servicios Sociales`.
- Santa Cruz de La Palma: `Organigrama`.
- Tazacorte: `Servicios Sociales` + referencia oficial indexada de `Órganos de Gobierno`.
- Tijarafe: `Concejalías`.
- Villa de Mazo: noticia institucional de reparto de áreas + `Servicios Sociales`.

## Dudas y problemas relevantes

- Los Llanos de Aridane: la web oficial del ayuntamiento muestra señales no totalmente consistentes sobre la titularidad nominal del área de Igualdad. Se dejó el contacto del área con `Nombre y apellidos = Unknown` para no forzar una atribución dudosa.
- San Andrés y Sauces: la página oficial de `Corporación Municipal` figura como `NO DISPONIBLE EN ESTOS MOMENTOS`. Se usó contacto operativo de `Servicios Sociales` con confianza media.
- Tazacorte: la referencia oficial de `Órganos de Gobierno` aparece indexada con la delegación exacta, pero no fue establemente recuperable en lectura directa. Se combinó con la página oficial actual de `Servicios Sociales`.
- Breña Alta, Breña Baja y Tijarafe: la identificación política/competencial es clara, pero los correos públicos estaban ausentes o protegidos, así que se priorizó teléfono directo o email general/servicio.
- Santa Cruz de La Palma: se localizó email personal institucional muy bueno, pero no teléfono visible en la lectura disponible.

## Criterio aplicado

- Se priorizó cobertura oficial y utilidad práctica sobre perfección de email.
- Cuando hubo nombre + cargo oficiales pero sin correo visible, se dejó `Unknown` en email y se mantuvo teléfono directo o general.
- No se inventaron emails ni se dedujeron patrones.
- Cuando la web municipal mostraba contradicciones o huecos, se rebajó la confianza y se dejó constancia en la última columna del CSV.

## Listo para consolidación

- El CSV ya usa exactamente el mismo header que `05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv`.
- No se tocaron otros archivos fuera de `la_palma.csv` y `la_palma.md`.
