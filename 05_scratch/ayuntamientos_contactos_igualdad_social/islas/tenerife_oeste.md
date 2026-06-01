# Tenerife oeste / centro

Cobertura completada para los 16 municipios pedidos en [tenerife_oeste.csv](/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling/05_scratch/ayuntamientos_contactos_igualdad_social/islas/tenerife_oeste.csv).

## Resumen

- Municipios cubiertos: 16/16
- Filas totales: 16
- Confianza `Alto`: 9
- Confianza `Medio`: 7
- Prioridad `Alta`: 12
- Prioridad `Media`: 4

## Criterio aplicado

- Una fila recomendada por municipio, priorizando igualdad, bienestar social y accion social.
- Solo se usaron fuentes oficiales municipales: areas municipales, corporacion/grupo de gobierno, directorios, sedes o noticias institucionales.
- No se dedujeron correos. Cuando no hubo email personal, se uso el del area o, si tampoco existia, el generico municipal con confianza mas baja.
- Cuando la web oficial no publicaba claramente a la persona titular, se dejo `Unknown` y se explico en la ultima columna.

## Fuentes oficiales usadas

- Adeje: `Igualdad y diversidad > Servicios` y `Area de Politicas de Igualdad`.
- Arafo: `Equipo de Gobierno`, `Bienestar Social` y un PDF oficial del ayuntamiento para recuperar el correo general de registro.
- Arico: pagina oficial de `Bienestar Social`.
- Buenavista del Norte: pagina oficial de `Igualdad` y `Grupo de Gobierno`.
- Candelaria: pagina oficial de `Igualdad`, `Servicios Sociales` y `Corporacion Local`.
- El Rosario: pagina oficial `Accion Social e Igualdad` y noticia institucional con telefono/email operativo del area.
- El Sauzal: `Corporacion Municipal del Mandato 2023-2027` actualizada en 2026 y actividad oficial `Mujer Sauzalera 2026`.
- El Tanque: pagina oficial de `Bienestar Social` y `Grupo Gobierno`.
- Fasnia: paginas oficiales de `Servicios Sociales`, `Igualdad`, `Telefonos municipales` y `Equipo de Gobierno 2023-2027`.
- Garachico: ficha oficial de `Maria Candelaria Perez Gonzalez`.
- Guia de Isora: pagina oficial de `Servicios Sociales` y `Alcaldesa y Concejales`.
- Guimar: ficha oficial de `Pedro Daniel Perez Rodriguez`.
- Icod de los Vinos: pagina oficial de `Grupo de Gobierno`.
- La Guancha: `Corporacion Municipal` y `Telefonos y Emails`.
- Puerto de la Cruz: area oficial `Derecho Social` y subpagina de `Servicios Sociales`.
- San Juan de la Rambla: `Grupo de Gobierno` y pagina oficial de `Servicios Sociales`.

## Dudas y validacion manual pendiente

- Adeje: no localice en abierto el nombre de la persona titular actual de la concejalia de igualdad; queda canal directo del area.
- Arafo: falta email especifico del area o de la concejala; el mejor fallback visible fue `registro@arafo.es`.
- Arico: la web oficial revisada no permitio cerrar con seguridad una titularidad nominal unica y actual para bienestar/igualdad; se priorizo el email del area.
- El Rosario: no quedo confirmada en texto una responsable politica actual de Accion Social e Igualdad; por prudencia no se uso un nombre potencialmente desactualizado.
- Fasnia: el correo que publica la propia web oficial de servicios sociales es Gmail; se mantiene por ser la fuente municipal visible, pero con confianza media.
- Guia de Isora: conviene validar si existe email personal institucional publico de Acerina Gonzalez Prieto y la formulacion exacta de su tenencia.
- Icod de los Vinos: la pagina oficial deja muy claro el area y el email de la concejala, pero no muestra telefono directo ni un correo generico especifico de Accion Social.
- Puerto de la Cruz: no localice en las paginas accesibles el nombre de la persona responsable actual del area; se entrega el canal operativo del area con sus UTS.
- San Juan de la Rambla: la titularidad politica es clara, pero falta email especifico del area o de la concejala.

## Problemas tecnicos

- Varias webs municipales ofuscan correos, los insertan como imagen o los dejan fuera del HTML principal; cuando no fue legible en abierto se bajo confianza.
- En algunos ayuntamientos hubo pequeñas tensiones entre pagina de area y pagina de gobierno; en esos casos se priorizo el contacto operativo oficial y se anoto la duda.
- En Tenerife oeste/centro abundan areas validas por telefono y concejalia, pero no siempre por email personal.

## Listo para consolidacion

- El CSV usa exactamente el mismo header que `05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv`.
- Hay una fila recomendada por cada uno de los 16 municipios pedidos.
- Solo se tocaron `tenerife_oeste.csv` y `tenerife_oeste.md`.
