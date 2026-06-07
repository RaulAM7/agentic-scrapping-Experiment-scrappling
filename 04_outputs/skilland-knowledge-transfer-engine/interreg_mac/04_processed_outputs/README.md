# Processed outputs

Esta carpeta alojara datasets procesados.

En este caladero, `processed` significa dataset intermedio listo para analisis, scoring o enrichment posterior. No implica que el registro ya sea un lead listo para outreach.

Tipos de output:

- datasets normalizados;
- datasets scored;
- datasets filtrados por geografia;
- datasets filtrados por topic;
- datasets enriquecidos;
- rankings.

No guardar raw data aqui.

Regla operativa:

- cualquier export final de prospeccion debe incluir `email` o `email_status`;
- mientras `contact_email` siga vacio, el dataset processed debe tratarse como pre-outreach.
