# Source Discovery Report - ICP2 Asociaciones / ONG - Mujeres e Inclusion Tech

Fecha: 2026-06-12

## Resumen ejecutivo

La evidencia apunta a una estrategia de `Opcion D - enfoque mixto`:

- Canarias V1 esta listo para una extraccion controlada, empezando por fuentes de alta calidad outbound y encaje tematico claro.
- Las fuentes canarias de mayor calidad son directorios o redes con seleccion previa: ICI, Tenerife Violeta, Tenerife Isla Solidaria, Red Anagos, EAPN Canarias, Plena Inclusion Canarias y Coordinadora ONGD Canarias.
- Las fuentes canarias de mayor volumen son datasets publicos y registros administrativos: Asociaciones de Canarias, Fundaciones de Canarias y Registro Regional de Entidades Colaboradoras de Servicios Sociales.
- Espana V2 debe quedar como mapa de caladeros para escalado: registros nacionales/autonomicos, redes estatales de mujeres/STEAM, plataformas del tercer sector, coordinadoras sectoriales y directorios de ONG.
- No conviene hacer scraping frio general antes de explotar las fuentes estructuradas y tematicas.

Esta fase no produce leads finales, no mezcla Espana con Canarias y no crea ficheros `organizations_clean.csv` ni `contacts_clean.csv`.

## Criterios usados

Cada fuente se evaluo por dos ejes:

- Volumen potencial: numero aproximado de organizaciones/contactos, cobertura territorial, posibilidad de filtrar por Canarias, isla, municipio, CCAA, mujeres, igualdad, STEAM, empleo, formacion, inclusion, migracion, juventud, emprendimiento o vulnerabilidad.
- Calidad outbound: presencia de personas con nombre y apellidos, cargo, email personal/institucional, email generico fiable, web, telefono, formulario, actividad verificable y posibilidad de crear `personalizacion_1` segura.

Tambien se marco esfuerzo de extraccion, valor como fuente primaria, valor de enriquecimiento, cautelas legales y prioridad por ronda.

## Canarias V1 - Discovery profundo

### Caladeros de mejor calidad outbound

Estas fuentes no son necesariamente las mas grandes, pero tienen mejor encaje para primeras tandas prudentes:

- ICI - Asociaciones y colectivos de mujeres: fuente tematica directa para `mujeres_igualdad_steam`. Su valor esta en el encaje, no en el volumen. Requiere revision de paginas insulares y validacion manual de contactos.
- Tenerife Violeta - Entidades comprometidas: red insular de igualdad con listado de entidades publicas, sociales y privadas. Buena para detectar entidades con compromiso explicito en igualdad y generar personalizacion segura.
- Tenerife Isla Solidaria - Asociaciones: directorio insular de entidades de voluntariado. Buen punto para entidades sociales con web/contacto y posterior filtrado por mujeres, inclusion, empleo o formacion.
- Red Anagos: red canaria de economia social y solidaria con entidades de inclusion, justicia social y desarrollo comunitario. Alta afinidad para `inclusion_tecnologica_impacto_social`.
- EAPN Canarias: agrupa entidades contra pobreza y exclusion social en Canarias. Buen encaje para inclusion, vulnerabilidad, migracion, empleo y brecha digital.
- Plena Inclusion Canarias: movimiento asociativo con entidades por isla; util para inclusion, empleo con apoyos y tecnologia accesible, aunque no siempre mujeres como foco principal.
- Coordinadora ONGD Canarias: directorio sectorial de ONGD con encaje en cooperacion, migracion, DDHH, igualdad y educacion para la ciudadania.

### Caladeros de mayor volumen

Estas fuentes aportan masa critica, pero requieren limpieza, filtrado y enriquecimiento:

- CSV Asociaciones de Canarias: fuente de volumen principal. Permite filtrar por denominacion, finalidad o territorio si el dataset lo contiene, pero normalmente no aporta personas ni emails personales. Debe usarse tras definir keywords ICP2 y reglas de descarte.
- CSV Fundaciones de Canarias: volumen medio, buena trazabilidad administrativa y filtros de finalidad/provincia/isla/municipio en el buscador. Requiere enriquecimiento de webs y contactos.
- Registro Regional de Entidades Colaboradoras en Servicios Sociales: fuente de volumen social con contacto y areas de prestacion. Mejor encaje que un registro general de asociaciones, porque ya restringe a accion social.
- Directorios insulares/voluntariado: Tenerife, La Palma y otros directorios insulares pueden aportar entidades locales con contacto util, pero requieren normalizacion por isla y deduplicacion.
- BOC/subvenciones ICI: util para identificar asociaciones activas en convocatorias de mujeres/igualdad; no debe usarse como fuente primaria de contacto sin contrastar en web oficial.

### Fuentes con personas/cargos/emails

En Canarias, la disponibilidad de personas con nombre y cargo es desigual:

- Mejor probabilidad: paginas de red/federacion con equipo, junta directiva o secretaria tecnica; webs propias de entidades descubiertas desde EAPN, Red Anagos, Plena Inclusion, Coordinadora ONGD Canarias o Tenerife Isla Solidaria.
- Probabilidad media: Tenerife Violeta y Consejos/organos de igualdad pueden incluir entidades y representantes, pero requieren revision manual.
- Baja probabilidad: CSV de asociaciones, CSV de fundaciones y registros administrativos. Suelen ser organizacion-only o contacto generico.

Por tanto, la primera extraccion debe separar organizacion de contacto y marcar `contact_quality` sin inventar personas ni cargos.

### Fuentes solo organizacion

Principalmente:

- CSV Asociaciones de Canarias.
- CSV Fundaciones de Canarias.
- Registro Nacional de Asociaciones cuando se use para Espana V2.
- Registros autonomicos generales.

Estas fuentes son utiles para volumen, deduplicacion, trazabilidad y enriquecimiento, no para cold outbound directo sin paso adicional.

### Fuentes de enriquecimiento en Canarias

- BOC y notas de subvenciones ICI: actividad reciente, beneficiarias y programas.
- Paginas institucionales de igualdad, juventud, voluntariado y servicios sociales.
- Directorios insulares: telefono, web, territorio e indicios de actividad.
- Webs propias de entidades detectadas: contacto real, actividad actual y personalizacion segura.

## Espana V2 - Discovery amplio nacional/sectorial/autonomico

### Caladeros nacionales de alta calidad

Estas fuentes merecen fase Espana V2 porque combinan encaje tematico, trazabilidad y potencial contacto:

- Consejo de Participacion de la Mujer: organo consultivo con representacion de asociaciones de mujeres. Alto valor para `mujeres_igualdad_steam`, bajo/medio volumen y alta necesidad de revision manual.
- Alianza STEAM por el talento femenino: red de entidades adheridas con foco claro en talento femenino y STEAM. Alta afinidad con la propuesta SkilLand IA Mujeres.
- AMIT, MujeresTech y Women in AI Spain: redes sectoriales de mujeres en ciencia/tecnologia/IA. Volumen bajo/medio, pero calidad outbound alta.
- ASEME, FEDEPE y redes de mujeres empresarias/directivas: encaje con liderazgo, emprendimiento y talento femenino.
- Federacion de Mujeres Progresistas y Fundacion Mujeres: alta afinidad tematica, potencial de red territorial y actividad verificable.
- Red Acoge: red estatal especializada en migracion y acogida; buena para inclusion, formacion, empleabilidad y genero cuando haya senal explicita.
- Plataforma de ONG de Accion Social, EAPN Espana y Coordinadora ONGD Espana: redes estatales con directorios y estructura territorial.
- Fundacion Lealtad: buscador de ONG acreditadas con filtros y trazabilidad. Buena fuente de calidad y enriquecimiento.

### Caladeros nacionales de alto volumen

Estas fuentes pueden aportar muchas entidades, pero exigen filtrado, limpieza y enriquecimiento:

- Registro Nacional de Asociaciones.
- Buscador de fundaciones de competencia estatal.
- AECID - Buscador de ONGD.
- Hacesfalta - Directorio de ONG.
- Plataforma del Tercer Sector y su entorno de redes.
- Registros autonomicos de asociaciones y fundaciones.

No deben explotarse en frio sin reglas de filtrado ICP2, deduplicacion y validacion manual de fuentes de contacto.

### Fuentes autonomicas futuras

Las comunidades autonomas son el principal backlog de escalado despues de Canarias:

- Andalucia: el IAM documenta mas de 2.000 asociaciones y federaciones de mujeres; es la fuente autonomica de mujeres con mayor volumen detectado.
- Comunitat Valenciana: directorio de asociaciones en datos abiertos, util para volumen y filtros territoriales.
- Euskadi/Emakunde: asociacionismo de mujeres, directorios y organos consultivos.
- Castilla-La Mancha: organo de consulta y participacion con asociaciones de mujeres representadas; fuente de alta calidad pero manual.
- Madrid: recursos y entidades de mujeres/vulnerabilidad, requiere localizar directorio explotable.
- Illes Balears: IBDONA y recursos/organos con asociaciones de mujeres; mas util para revision manual que para volumen.
- Aragon, Galicia y otras CCAA: fuentes oficiales de igualdad y registros generales; candidatas a ronda 5.

## Alto volumen

Fuentes de mayor volumen potencial:

- Registro Nacional de Asociaciones.
- Registros autonomicos de asociaciones.
- CSV Asociaciones de Canarias.
- Instituto Andaluz de la Mujer - listado de asociaciones/federaciones de mujeres.
- AECID - Buscador de ONGD.
- Hacesfalta - Directorio de ONG.
- Plataforma del Tercer Sector y redes estatales.
- Fundacion Lealtad - ONG acreditadas.
- Registro Regional de Entidades Colaboradoras de Servicios Sociales de Canarias.

## Alta calidad outbound

Fuentes con mejor probabilidad de encaje y personalizacion segura:

- ICI asociaciones/colectivos de mujeres.
- Tenerife Violeta.
- Red Anagos.
- EAPN Canarias.
- Plena Inclusion Canarias.
- Coordinadora ONGD Canarias.
- Consejo de Participacion de la Mujer.
- Alianza STEAM por el talento femenino.
- AMIT, MujeresTech, Women in AI Spain.
- ASEME, FEDEPE, Federacion de Mujeres Progresistas, Fundacion Mujeres.
- Red Acoge, Coordinadora ONGD Espana, Plataforma ONG Accion Social, Fundacion Lealtad.

## Gaps detectados

- Muchas fuentes de volumen no incluyen personas con cargo ni email personal.
- Algunas fuentes de igualdad son listas institucionales o redes, no directorios descargables.
- Los directorios insulares no siguen un formato comun y requeriran normalizacion.
- Las fuentes autonomicas no son homogeneas: algunas tienen CSV, otras buscador, otras solo paginas informativas o organos consultivos.
- La informacion de actividad puede estar desactualizada en registros administrativos.
- Para cold outbound, la revision humana sigue siendo obligatoria antes de usar cualquier email publicado.

## Conclusion

Canarias V1 tiene fuentes suficientes para empezar una extraccion controlada en la siguiente fase. La mejor secuencia es:

1. Canarias alta calidad: directorios y redes con encaje explicito.
2. Canarias volumen: registros y CSV para ampliar base y enriquecer.
3. Espana nacional alta calidad: redes tematicas mujeres/STEAM/ONG.
4. Espana nacional alto volumen: registros y buscadores grandes.
5. CCAA: escalado territorial empezando por fuentes autonomicas de mujeres e igualdad con mejor volumen o estructura.

No se recomienda empezar por scraping frio general.
