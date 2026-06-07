# Scrapers

Esta carpeta alojara scripts y experimentos de scraping para keep.eu / Interreg MAC.

## Subcarpetas

- `experiments/`: pruebas pequenas de extraccion.

## Reglas

- Empezar siempre con samples pequenos.
- No lanzar scraping masivo sin source assessment.
- Respetar robots/terms.
- Usar delays.
- Cachear.
- Loguear fuente y fecha.
- No mezclar raw y processed.
- No confundir `partner scored` con lead final: si falta email, el scraping aun no ha terminado.
