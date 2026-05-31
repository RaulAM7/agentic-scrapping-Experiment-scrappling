# Scraping waves plan — Interreg MAC / keep.eu

## Wave 0 — Source discovery

Objetivo:

- inspeccionar keep.eu;
- entender filtros;
- entender export;
- entender API/endpoints si existen;
- revisar robots/terms;
- documentar metodo limpio.

Output:

- assessment de fuente;
- decision de extraccion;
- lista de URLs/paginas relevantes.

Notas para este caladero:

- confirmar si MAC 2021-2027 existe como programa publico en keep.eu;
- definir si el arranque se hace por programa MAC 2014-2020, por outermost regions, por Atlantic Area o por combinacion de geografia + topics;
- preparar solicitud de API key si se decide escalar.

## Wave 1 — Mini sample

Objetivo:

- extraer muestra pequena de 20-50 registros;
- validar campos;
- validar scoring;
- detectar duplicados;
- revisar calidad de datos;
- detectar si Interreg MAC aparece bien filtrado.

Output:

- sample raw;
- sample processed;
- mini report.

Notas para este caladero:

- usar primero export GUI o URLs estables;
- priorizar registros con `Only ongoing projects` cuando existan;
- si MAC 2021-2027 sigue `Unknown`, usar sample mixto:
  - MAC 2014-2020;
  - outermost regions;
  - Atlantic Area;
  - queries con training, capacity building, SME support y entrepreneurship.

## Wave 2 — Interreg MAC reciente

Objetivo:

- extraer proyectos y partners 2021-2027;
- priorizar proyectos activos o recientes;
- aplicar taxonomia;
- generar dataset procesado.

Output:

- dataset Interreg MAC raw;
- dataset Interreg MAC scored.

Condicion:

- solo ejecutar esta wave como `Interreg MAC reciente` cuando quede confirmado el acceso limpio a ese subconjunto en keep.eu.

## Wave 3 — Expansion geografica

Objetivo:

- Espana;
- Portugal;
- Italia;
- Canarias;
- Madeira;
- Azores;
- Cabo Verde;
- Mauritania;
- Senegal;
- Marruecos;
- Atlantico/Mediterraneo.

Output:

- datasets por geografia;
- ranking de entidades/proyectos.

## Wave 4 — Enriquecimiento web

Objetivo:

- ir a webs oficiales de proyecto;
- webs de partner;
- documentos;
- paginas de contacto;
- outputs visibles;
- senales formativas.

Output:

- dataset enriched;
- report de mejores oportunidades.

## Wave 5 — Dataset final de scraping

Objetivo:

- dataset limpio;
- deduplicado;
- scored;
- con fuente trazable;
- listo para que otro proceso/agente lo use.
