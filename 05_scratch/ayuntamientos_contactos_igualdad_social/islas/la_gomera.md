# La Gomera

## Resumen

- Municipios cubiertos: 6/6.
- Criterio aplicado: una fila util por municipio, priorizando igualdad y servicios sociales, con fuente oficial municipal y sin inventar emails.
- Resultado: 4 municipios con persona responsable identificada; 2 municipios con area/unidad confirmada pero sin responsable visible en abierto.

## Fuentes oficiales usadas

### Agulo

- Sede electronica, directorio de la organizacion:
  `https://eadmin.agulo.org/public/ddlo/directorio.aspx`

### Alajero

- Pagina oficial de Servicios Sociales:
  `https://www.ayuntamientoalajero.es/index.php/el-ayto/servicios-sociales`
- Noticia oficial que identifica a Agueda Franquis como concejala de Servicios Sociales:
  `https://www.ayuntamientoalajero.es/index.php/prensa/noticias-2025/1036-el-ayuntamiento-de-alajero-convoca-proceso-selectivo-para-lista-de-reserva-para-trabajador-o-trabajadora-social`

### Hermigua

- Grupo de gobierno:
  `https://villadehermigua.com/ayuntamiento/grupo-de-gobierno.html`
- Dependencias y contacto:
  `https://www.villadehermigua.com/ayuntamiento/dependencias-y-contacto.html`

### San Sebastian de La Gomera

- Area municipal de Politicas Sociales e Igualdad:
  `https://sansebastiangomera.org/areas-municipales/politicas-sociales-igualdad/`
- Sede electronica, directorio:
  `https://eadmin.sansebastiangomera.org/public/ddlo/directorio.aspx`
- Directorio telefonico municipal:
  `https://www.sansebastiangomera.org/directorio-telefonico/`

### Valle Gran Rey

- Portal de transparencia, miembros electos:
  `https://transparencia.vallegranrey.es/personal-libre-nombramiento/miembros-electos/`
- Decreto oficial de delegacion de competencias:
  `https://transparencia.vallegranrey.es/media/r/institucional/sesiones-y-actas/2024%20Actas/Decreto%20modificaci%C3%B3n%20delegaci%C3%B3n%20de%20competencias%20gobierno%20municipal.pdf`

### Vallehermoso

- Sede electronica, directorio:
  `https://eadmin.vallehermosoweb.es/publico/directorio`
- Aviso legal / datos generales del portal:
  `https://eadmin.vallehermosoweb.es/publico/contenido/AVLEGAL`

## Dudas y validacion manual pendiente

- Agulo: no localice en fuente municipal visible el nombre del concejal o concejala responsable de Asuntos Sociales.
- Hermigua: no localice email de area ni email personal del concejal; solo contacto municipal generico.
- San Sebastian de La Gomera: no localice email publico del area de Politicas Sociales e Igualdad; queda email de Alcaldia como fallback.
- Valle Gran Rey: el contacto util es claro, pero el email accesible es generico municipal.
- Vallehermoso: no localice en abierto el nombre de la persona responsable de la concejalia social/igualdad.

## Problemas tecnicos

- Varias sedes electronicas muestran mejor las unidades y los correos que las webs publicas, pero no siempre exponen la persona responsable.
- En Vallehermoso fue necesario tirar de la sede y del footer/directorio; la identificacion del cargo politico sigue incompleta.
- En Alajero el email del area estaba protegido en la web y hubo que leer el HTML oficial para confirmarlo; no se dedujo ningun patron.

## Criterio de consolidacion recomendado

- Integrar estas 6 filas como lote La Gomera.
- Mantener `Unknown` donde falta nombre o email especifico.
- Si despues se hace una pasada de refinado, priorizar solo Agulo y Vallehermoso para sacar nombre politico responsable y San Sebastian / Hermigua / Valle Gran Rey para afinar email de area.
