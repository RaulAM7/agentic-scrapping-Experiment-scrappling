# ICP: Asesorias Fiscales y Contables Independientes — Canarias
> Status: draft
> Generated: 2026-03-07
> Beachhead: yes
> Confidence: medium

## 1. Target Org
| Atributo | Valor | Confianza |
|----------|-------|-----------|
| Sector vertical | Asesoria fiscal, contable, o fiscal-contable | stated |
| Tamano equipo | 1-50 profesionales (incluye titular autonomo solo) | inferred |
| Volumen clientes | 50-300 clientes activos | stated |
| Geografia | Islas Canarias (Las Palmas, Tenerife prioritarios) | stated |
| Modelo de negocio | Cuota mensual fija por cliente, a veces colaboracion con plataformas nacionales | stated |

## 2. Trigger Events
| Evento | Ventana temporal | Confianza |
|--------|-----------------|-----------|
| Cierre trimestral fiscal (enero, abril, julio, octubre) | 2-4 semanas antes de cada cierre | stated |
| Campana Impuesto Sociedades (julio) | Abril-julio | stated |
| Frustracion acumulada con software contable legacy (Dias Software/Cegid, A3, Sage) | Continuo, picos en cierres trimestrales | inferred |
| Crecimiento de cartera sin capacidad de contratar | Cuando supera ~100 clientes sin empleados | inferred |
| Cambio normativo fiscal Canarias (REF, IGIC) | Tras publicacion en BOC/BOE | hypothesis |

## 3. Decision Unit

**Buyer** — Titular del despacho / autonomo principal: ahogado en trabajo operativo manual que le impide ofrecer servicios de mayor valor. Motivador: recuperar tiempo para asesoramiento estrategico, formacion y calidad de vida.

**User** — Mismo titular + auxiliares administrativos: ejecutan la clasificacion documental, escaneo de facturas, conciliacion trimestral y comunicacion con clientes.

**Blocker** — Omitido. En despachos de 1-5 personas el titular es comprador y usuario. No hay estructura de veto separada.

## 4. Observable Signals

### Web / Presencia Digital
| Signal | Query Hint | Confianza | Check Type |
|--------|-----------|-----------|------------|
| Web basica o inexistente (sin blog, sin portal cliente) | Buscar dominio; verificar si tiene web propia o solo Google Business | inferred | automated |
| Sin portal de subida de documentos para clientes | Revisar si la web ofrece area de cliente o upload | inferred | automated |
| Mencion de servicios: contabilidad, fiscalidad, IGIC, autonomos, sociedades | Scrape de pagina de servicios o descripcion Google Business | inferred | automated |
| Presencia solo en directorios (Paginas Amarillas, QDQ, Google Maps) sin web propia | Buscar nombre en Google, verificar si resultado es directorio vs web propia | inferred | automated |

### Registros / Directorios Publicos
| Signal | Query Hint | Confianza | Check Type |
|--------|-----------|-----------|------------|
| Alta en RECC (Registro de Economistas Censores) o colegio profesional | Buscar en registros colegiales de Canarias | stated | automated |
| Registro en Colegio de Gestores Administrativos de Las Palmas/Santa Cruz | Directorio publico del colegio | inferred | automated |
| Alta como autonomo en epigrafe IAE 841/842 (servicios contables/fiscales) | No accesible directamente, pero correlaciona con listados colegiales | inferred | manual_check |
| Antiguedad del negocio > 5 anos | Registro Mercantil o Google Business "abierto desde" | inferred | automated |
| Ubicacion en Las Palmas de GC o Santa Cruz de Tenerife (capitales insulares) | Google Maps / directorio, filtrar por localidad | stated | automated |

### Google Maps / Google Business
| Signal | Query Hint | Confianza | Check Type |
|--------|-----------|-----------|------------|
| Ficha de Google Business activa con categoria "asesoria fiscal" o "gestoria" | Buscar "asesoria fiscal Las Palmas" / "gestoria contable Tenerife" en Google Maps | stated | automated |
| Resenas que mencionan atencion personalizada, cercania, trato directo | Scrape de resenas Google; buscar keywords: "trato", "cercano", "rapido", "confianza" | inferred | automated |
| Horario publicado de oficina (indica operacion presencial tradicional) | Campo horario en Google Business | inferred | automated |
| Fotos de oficina pequena / despacho individual | Google Business > fotos | inferred | manual_check |

### LinkedIn
| Signal | Query Hint | Confianza | Check Type |
|--------|-----------|-----------|------------|
| Perfil personal del titular (no pagina de empresa) como unico punto de presencia | Buscar nombre + "asesor fiscal" + "Canarias" en LinkedIn | inferred | automated |
| Sin pagina de empresa en LinkedIn o con < 5 seguidores | Buscar nombre del despacho en LinkedIn Companies | inferred | automated |
| Descripcion de perfil menciona: autonomos, pymes, contabilidad, IGIC, Canarias | Scrape de headline/about del perfil | inferred | automated |

## 5. Anti-ICP
| Exclusion | Razon |
|-----------|-------|
| Grandes firmas de auditoria (Big 4, BDO, Grant Thornton) | Sin dolor operativo individual; procesos corporativos, no compradores validos |
| Gestoria laboral pura (sin componente fiscal/contable) | Dolor diferente; flujo documental distinto |
| Despachos ya digitalizados con portal cliente y ERP cloud moderno | Pain resuelto; no hay urgencia de compra |
| Sector publico / administracion | Ciclos de compra incompatibles, no es el buyer |
| Asesorias con > 20 empleados | Estructura interna absorbe el dolor; necesitan ERP enterprise, no nuestra solucion |

## 6. Scoring Heuristic
| Signal (o combinacion) | Peso (1-5) | Fuente |
|------------------------|-----------|--------|
| Ficha Google Business activa como asesoria fiscal/gestoria en Canarias | 4 | Google Maps |
| Sin web propia o web basica sin portal cliente | 3 | Web |
| Registro en colegio profesional (economistas/gestores) Canarias | 3 | Registros |
| Resenas Google mencionando trato personal/directo | 2 | Google Business |
| Solo perfil personal LinkedIn (sin pagina empresa) | 2 | LinkedIn |
| Ubicacion en Las Palmas o Santa Cruz | 2 | Google Maps |
| Sin portal cliente + registro colegial + resenas trato personal (combo) | 8 | Compuesto |
| Ficha Google Business + sin web propia + antiguedad > 5 anos (combo) | 7 | Compuesto |

## Changelog
| Fecha | Cambio | Razon |
|-------|--------|-------|
| 2026-03-07 | Generacion inicial | Contexto de proyecto + caso Yanira como validacion |

---

```yaml
---
# machine-readable ICP — do not edit manually, generated from content above
icp:
  segment: "Asesorias Fiscales y Contables Independientes — Canarias"
  status: draft
  confidence: medium
  beachhead: true
  generated: "2026-03-07"

  target_org:
    - attribute: "sector_vertical"
      value: "Asesoria fiscal, contable, o fiscal-contable"
      confidence: stated
    - attribute: "tamano_equipo"
      value: "1-10 profesionales"
      confidence: inferred
    - attribute: "volumen_clientes"
      value: "50-300 clientes activos"
      confidence: stated
    - attribute: "geografia"
      value: "Islas Canarias (Las Palmas, Tenerife prioritarios)"
      confidence: stated
    - attribute: "modelo_negocio"
      value: "Cuota mensual fija por cliente, colaboracion con plataformas nacionales"
      confidence: stated

  triggers:
    - event: "Cierre trimestral fiscal"
      window: "2-4 semanas antes de cada cierre (ene, abr, jul, oct)"
      confidence: stated
    - event: "Campana Impuesto Sociedades"
      window: "Abril-julio"
      confidence: stated
    - event: "Frustracion con software contable legacy"
      window: "Continuo, picos en cierres"
      confidence: inferred
    - event: "Crecimiento cartera sin capacidad contratar"
      window: "Al superar ~100 clientes sin empleados"
      confidence: inferred
    - event: "Cambio normativo fiscal Canarias"
      window: "Tras publicacion BOC/BOE"
      confidence: hypothesis

  decision_unit:
    buyer:
      role: "Titular del despacho / autonomo principal"
      pain: "Atrapado en trabajo operativo manual que consume ~1.5 semanas/mes"
      motivator: "Recuperar tiempo para asesoria estrategica, formacion y calidad de vida"
    user:
      role: "Titular + auxiliares administrativos"
      pain: "Clasificacion documental manual, OCR defectuoso, conciliacion trimestral"
    blocker:
      role: ""
      objection: ""

  signals:
    - signal: "Ficha Google Business como asesoria fiscal/gestoria en Canarias"
      source: "google_maps"
      query_hint: "Buscar 'asesoria fiscal Las Palmas' / 'gestoria contable Tenerife' en Google Maps"
      confidence: stated
      check_type: automated
    - signal: "Sin web propia o web basica sin portal cliente"
      source: "web"
      query_hint: "Verificar dominio; buscar area cliente o upload"
      confidence: inferred
      check_type: automated
    - signal: "Registro en colegio profesional Canarias"
      source: "registros"
      query_hint: "Directorio publico colegio economistas/gestores Canarias"
      confidence: inferred
      check_type: automated
    - signal: "Resenas Google mencionando trato personal"
      source: "google_business"
      query_hint: "Scrape resenas; keywords: trato, cercano, confianza"
      confidence: inferred
      check_type: automated
    - signal: "Solo perfil personal LinkedIn sin pagina empresa"
      source: "linkedin"
      query_hint: "Buscar nombre despacho en LinkedIn Companies"
      confidence: inferred
      check_type: automated
    - signal: "Ubicacion en capitales insulares"
      source: "google_maps"
      query_hint: "Filtrar por Las Palmas de GC o Santa Cruz de Tenerife"
      confidence: stated
      check_type: automated
    - signal: "Antiguedad negocio > 5 anos"
      source: "google_business"
      query_hint: "Campo 'abierto desde' en Google Business"
      confidence: inferred
      check_type: automated

  anti_icp:
    - exclusion: "Grandes firmas auditoria (Big 4, BDO)"
      reason: "Sin dolor operativo individual"
    - exclusion: "Gestoria laboral pura"
      reason: "Dolor y flujo documental diferente"
    - exclusion: "Despachos ya digitalizados con ERP cloud"
      reason: "Pain resuelto"
    - exclusion: "Sector publico"
      reason: "Ciclos compra incompatibles"
    - exclusion: "Asesorias con > 20 empleados"
      reason: "Necesitan ERP enterprise"

  scoring:
    - signal_ref: "Ficha Google Business asesoria fiscal Canarias"
      weight: 4
      source: "google_maps"
    - signal_ref: "Sin web propia o basica"
      weight: 3
      source: "web"
    - signal_ref: "Registro colegio profesional"
      weight: 3
      source: "registros"
    - signal_ref: "Resenas trato personal"
      weight: 2
      source: "google_business"
    - signal_ref: "Solo perfil personal LinkedIn"
      weight: 2
      source: "linkedin"
    - signal_ref: "Ubicacion capitales insulares"
      weight: 2
      source: "google_maps"
    - signal_ref: "Sin portal cliente + registro colegial + resenas trato personal"
      weight: 8
      source: "compuesto"
    - signal_ref: "Ficha Google + sin web propia + antiguedad > 5a"
      weight: 7
      source: "compuesto"
---
```
