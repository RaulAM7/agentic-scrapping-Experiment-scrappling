# Lanzarote

Cobertura completada para los 7 municipios de Lanzarote con un minimo de una fila util y recomendada por municipio en [lanzarote.csv](/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling/05_scratch/ayuntamientos_contactos_igualdad_social/islas/lanzarote.csv).

## Resumen

- Municipios cubiertos: 7/7
- Filas totales: 7
- Confianza `Alto`: 5
- Confianza `Medio`: 2
- Prioridad `Alta`: 7

## Fuentes oficiales usadas

- Arrecife: pagina oficial de la `Concejalia de Bienestar Social, Igualdad e Inmigracion` + noticia institucional reciente del area.
- Haria: noticia oficial del `Area de Bienestar Social` + pagina oficial de `Telefonos y Correos Electronicos`.
- San Bartolome: noticia institucional 2025 sobre programacion municipal + `Directorio Telefonico`.
- Teguise: `Concejales del Grupo de Gobierno` + pagina oficial de `Bienestar Social`.
- Tias: pagina oficial de la `Concejalia de Servicios Sociales y Participacion Ciudadana` + `Contacto`.
- Tinajo: noticia oficial de `Igualdad` + pagina de `Telefonos y Correos Electronicos de Interes Municipal`.
- Yaiza: pagina oficial de `Concejalias` + pagina oficial de `Servicios Sociales`.

## Dudas y problemas relevantes

- Arrecife: la responsable politica actual del area aparece como Maite Corujo en noticias oficiales recientes, pero no localice una ficha corporativa actual con email personal ni con el nombre formal completo.
- Haria: el email operativo es claro, pero la asignacion nominal a Chaxiraxi Niz se apoya en noticias oficiales y no en un organigrama simplificado con correos.
- San Bartolome: hay buena operatividad por los correos de `serviciossociales@` e `igualdad@`, pero conviene validar manualmente si la concejala idonea para personalizar el outreach de igualdad es Carmen Medina Toledo u otra edil del equipo.
- Tinajo: la Concejalia de Igualdad queda bien atribuida a Yurena Cubas en noticias oficiales, aunque el correo especifico visible de servicio sigue siendo el de Servicios Sociales.
- Yaiza: la titularidad politica y el telefono del area estan claros, pero la web oficial no expone un email especifico de Servicios Sociales ni correo personal institucional del concejal.

## Criterio aplicado

- Se priorizo fuente oficial municipal, cobertura completa y utilidad de outreach sobre perfeccion nominal.
- Cuando hubo concejal o concejala claramente identificable con email personal, se priorizo ese canal.
- Cuando no hubo email personal, se uso email del area o un fallback generico municipal sin inventar patrones.
- Se mantuvo `Unknown` en partido, email o canal especifico cuando la web oficial revisada no lo publicaba con claridad.

## Listo para consolidacion

- El CSV usa exactamente el mismo header que `05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv`.
- No se tocaron otros archivos fuera de `lanzarote.csv` y `lanzarote.md`.
