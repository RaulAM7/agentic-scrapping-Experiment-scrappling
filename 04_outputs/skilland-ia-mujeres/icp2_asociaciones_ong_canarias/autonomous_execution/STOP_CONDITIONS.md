# STOP_CONDITIONS - ICP2 Autonomous Execution

Fecha inicial: 2026-06-13

## Principio

Una futura `/goal` debe parar antes de producir basura, mezclar territorios, inventar datos o tocar sistemas comerciales.

## Stop conditions duras

Parar inmediatamente y actualizar `STATE.md` a `stopped_needs_human_review` si ocurre cualquiera:

- Se intenta tocar CRM.
- Se intenta tocar GWS.
- Se intenta enviar emails o preparar workflows.
- Se intenta modificar `04_outputs/skilland_ia_mujeres/data_prep/`.
- Se detecta email deducido por patron.
- Se inventa o no se puede justificar un cargo, persona, actividad o senal de encaje.
- Falta `source_url` en cualquier fila candidata a dataset limpio.
- Se mezcla Canarias V1 con Espana V2.
- Ronda 2 empieza sin reviewer PASS/PASS_WITH_WARNINGS de Ronda 1.
- Se activa scraping Espana V2 en esta autonomia.
- `git diff --check` falla y no se puede corregir sin cambiar scope.

## Stop por ruido

Parar la fuente y marcarla `manual_review` si:

- mas del 50% de una muestra inicial no encaja con ICP2;
- la fuente mezcla entidades sociales, administraciones, empresas y particulares sin separacion fiable;
- no hay forma de distinguir actividad social de actividad recreativa/general;
- la fuente devuelve entidades sin territorio verificable;
- el filtro por keywords captura ruido dominante.

Continuar con la siguiente fuente solo si:

- el fallo no afecta el canon de ronda;
- queda registrado en `ERRORS_AND_BLOCKERS.md`;
- no hay riesgo de contaminacion del dataset.

## Stop por exceso de Review

Parar la ronda si:

- Ronda 1 supera 40% de registros `Review`.
- Ronda 2 supera 50% de candidatos `Review`.
- Una fuente individual supera 60% `Review`.

Accion:

- no avanzar de ronda;
- documentar causas;
- preparar muestra para revision humana.

## Stop por emails

Parar una fuente si:

- aparecen emails sospechosos de patron;
- los emails no tienen pagina fuente;
- los emails pertenecen a dominios de terceros no explicados;
- hay muchos emails personales sin cargo/contexto;
- el parser extrae ruido tecnico o emails de tracking.

Si no aparecen emails:

- no parar automaticamente;
- crear `organization_only=true`;
- enviar a `organization_only.csv` o enrichment;
- no crear contacto inventado.

## Stop por datos personales

Parar la fuente o marcar manual review si:

- aparecen nombres/cargos en organos consultivos;
- aparecen emails personales publicados sin contexto de contacto institucional;
- hay datos sensibles o privados;
- la pagina parece antigua o no oficial.

Permitido:

- conservar la entidad;
- marcar `contact_quality=named_person_no_email` o `needs_manual_review=true`;
- no usar para outbound hasta revision humana.

## Stop por bloqueo tecnico

Parar fuente si:

- captcha;
- login;
- bloqueo por bot;
- rate limit;
- errores 403/429 repetidos;
- mas de 3 fallos consecutivos de fetch;
- estructura rota que impide trazabilidad.

Prohibido:

- insistir agresivamente;
- saltar controles;
- usar credenciales;
- usar fuentes privadas.

## Stop por volumen

Parar o degradar a backlog si:

- Ronda 1 fuente supera 300 entidades antes de filtros;
- Ronda 2 requiere enriquecer mas de 100 organizaciones por fuente en la misma corrida;
- el CSV/dataset es demasiado grande para QA manual razonable en la sesion;
- dedupe produce demasiados posibles duplicados sin resolver.

Accion:

- exportar solo muestra/candidatos filtrados;
- documentar backlog;
- pedir nueva fase si conviene ampliar.

## Stop por dedupe

Parar merge si:

- duplicados exactos no se resuelven;
- misma entidad aparece con webs/emails contradictorios;
- entidades nacionales aparecen como Canarias sin presencia verificable;
- una fuente de volumen duplica masivamente Ronda 1.

Accion:

- mantener fuentes separadas;
- marcar `duplicate_possible=true`;
- no promocionar a CRM.

## Stop por personalizacion

Parar promocion de un registro si:

- `personalizacion_1` requiere afirmar algo no publicado;
- la fuente solo da nombre y no actividad;
- se menciona IA/STEAM/mujeres sin evidencia;
- la entidad solo prueba inclusion general y se intenta usar copy de mujeres.

Accion:

- dejar `personalizacion_1` vacia;
- marcar `personalizacion_insegura`;
- enviar a Review si el registro depende de esa senal.

## Stop por QA final

No cerrar una futura `/goal` como completa si:

- falta `reviewer_report.md`;
- falta `data_quality_report.md`;
- falta `gaps_and_manual_review.md`;
- no existe `FINAL_SUMMARY.md` actualizado;
- `STATE.md` no refleja estado final;
- `EXECUTION_LOG.md` no tiene eventos por fuente;
- no se ejecuto `git diff --check`.
