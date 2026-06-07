# Scoring model — Interreg MAC / keep.eu

## 1. Objetivo

Priorizar proyectos, partners y entidades por encaje con `Skilland Knowledge Transfer Engine`.

La logica del score es priorizar no solo tema, sino capacidad real de activar transferencia de conocimiento con beneficiarios claros y entidades accionables.

Regla clave:

- `score` mide encaje comercial / estrategico;
- `lead_readiness` mide si el registro ya esta listo para outreach;
- un `Score 5` sin email sigue siendo un lead incompleto.

## 2. Score 5 — Muy alto encaje

Caracteristicas:

- proyecto reciente o activo;
- programacion 2021-2027;
- varios partners;
- entidad prioritaria;
- geografia prioritaria;
- senales claras de training, capacity building, knowledge transfer, dissemination o exploitation;
- beneficiarios empresariales, profesionales o emprendedores;
- outputs reutilizables;
- contacto o entidad accionable.

## 3. Score 4 — Alto encaje

Buen topic y entidad interesante, pero falta algun dato como contacto, rol, estado, evidencia formativa o detalle de beneficiarios.

## 4. Score 3 — Encaje medio

Senales parciales. Guardar para enriquecimiento.

## 5. Score 2 — Bajo encaje

Relacion indirecta con formacion o transferencia. No priorizar en primera ola.

## 6. Score 1 — Descartar

Sin formacion, sin transferencia, sin beneficiarios, proyecto antiguo sin continuidad o relacion muy debil.

## 7. Subscores

Definir subscores de `0` a `5`:

- `recency_score`
- `geo_score`
- `topic_score`
- `training_transfer_score`
- `beneficiary_score`
- `entity_type_score`
- `data_quality_score`
- `commercial_relevance_score`

Guia corta por subscore:

### recency_score

- `5`: activo o muy reciente; 2021-2027.
- `4`: 2021-2027 sin prueba fuerte de actividad reciente.
- `3`: 2014-2020 con outputs vivos o continuidad.
- `2`: 2014-2020 sin continuidad visible.
- `1`: antiguo o poco claro.
- `0`: sin fecha util.

### geo_score

- `5`: Espana, Portugal, Italia, Canarias, Madeira, Azores.
- `4`: Cabo Verde, Mauritania, Senegal, Marruecos.
- `3`: resto Atlantico/Mediterraneo cercano.
- `2`: geografia europea menos prioritaria pero util.
- `1`: geografia periferica para el arranque.
- `0`: geografia irrelevante o desconocida.

### topic_score

- `5`: training, capacity building, knowledge transfer, SME support, entrepreneurship.
- `4`: digital transformation, skills, mentoring, methodology, toolkit.
- `3`: innovation, pilot, dissemination o exploitation con poca prueba.
- `2`: topic tangencial.
- `1`: topic debil.
- `0`: sin topic util.

### training_transfer_score

- `5`: evidencia textual clara de academia, cursos, materiales, metodologia, training schemes o transferencia.
- `4`: evidencia clara de dissemination/exploitation con outputs convertibles.
- `3`: evidencia parcial.
- `2`: menciones vagas.
- `1`: muy debil.
- `0`: nula.

### beneficiary_score

- `5`: SMEs, emprendedores, profesionales, workforce o tejido productivo claramente definidos.
- `4`: beneficiarios definidos pero no empresariales.
- `3`: beneficiarios indirectos o mixtos.
- `2`: beneficiarios poco claros.
- `1`: beneficiarios vagos.
- `0`: sin beneficiarios visibles.

### entity_type_score

- `5`: camara, cluster, agencia de desarrollo, agencia de innovacion, universidad, centro tecnologico.
- `4`: fundacion, autoridad publica, organismo de empleo, entidad de emprendimiento.
- `3`: asociacion o actor mixto con rol util.
- `2`: socio tecnico sin activacion clara.
- `1`: entidad poco accionable.
- `0`: entidad irrelevante o desconocida.

### data_quality_score

- `5`: ficha clara, descripcion util, geografia, programa y rol visibles.
- `4`: faltan pocos datos.
- `3`: datos suficientes para guardar.
- `2`: datos incompletos.
- `1`: datos pobres.
- `0`: datos inutiles.

### commercial_relevance_score

- `5`: la entidad parece capaz de comprar, liderar, coordinar o activar formacion.
- `4`: buena capacidad institucional pero menos clara.
- `3`: potencial medio.
- `2`: potencial bajo.
- `1`: muy bajo.
- `0`: nulo.

## 8. Ponderacion sugerida

Formula sugerida:

- `recency_score`: 15%
- `geo_score`: 15%
- `topic_score`: 20%
- `training_transfer_score`: 20%
- `beneficiary_score`: 10%
- `entity_type_score`: 10%
- `data_quality_score`: 5%
- `commercial_relevance_score`: 5%

Formula compacta:

`score_total = recency*0.15 + geo*0.15 + topic*0.20 + training_transfer*0.20 + beneficiary*0.10 + entity_type*0.10 + data_quality*0.05 + commercial_relevance*0.05`

Escala final sugerida:

- `4.5 - 5.0`: prioridad A
- `3.8 - 4.4`: prioridad B
- `3.0 - 3.7`: prioridad C
- `2.0 - 2.9`: parking
- `< 2.0`: descarte

## 9. Reglas anti-falsos positivos

No puntuar alto solo por:

- innovation;
- digital;
- cooperation;
- sustainability;
- green;
- platform;
- project.

Debe haber senal real de:

- transferencia;
- formacion;
- beneficiarios;
- outputs;
- o capacidad de activacion.

Checks minimos antes de subir a `Score 4` o `Score 5`:

- texto que apunte a training, dissemination, exploitation o methodology;
- beneficiario identificable;
- entidad o partner accionable;
- geografia y periodo consistentes con la prioridad.

## 10. Capa de contactabilidad

Campos minimos que deben existir antes de exportar a outreach:

- `contact_name` si existe;
- `contact_role` si existe;
- `email` o `contact_email`;
- `email_status` si no hay email;
- `contact_url`;
- `email_source_url`;
- `lead_readiness`.

Enum recomendado para `email_status`:

- `email_found`
- `email_not_found_no_website`
- `email_not_found_no_contact_channel`
- `email_not_found_form_only`
- `email_not_found_scrape_blocked`
- `email_not_found_manual_review`

Estados recomendados para `lead_readiness`:

- `ready_for_outreach`
- `not_outreach_ready`
- `manual_review_needed`
