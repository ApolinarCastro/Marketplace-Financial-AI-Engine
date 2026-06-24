# Marketplace XML ↔ Ledger Completeness Certification

> **Fecha:** 2026-06-03
> **Tipo:** Forense — READ ONLY
> **Fuente:** `data/db/meli_financial_v4.db` + filesystem XMLs
> **Muestra estadística:** 100 transacciones aleatorias por marketplace

---

## Resumen Ejecutivo

**Completitud bidireccional NO certificada para ningún marketplace.**

| Marketplace | Ledger → XML (folio_xml) | XML → Ledger (Folio match) | Dashboard Badge | Gap Real |
|---|---|---|---|---|
| **ML** | 89.4% rows / 62.0% $ | 0% por Folio / 100% por monto+fecha | **FALSO POSITIVO** | $12.6M |
| **PARIS** | 79.0% rows / 82.6% $ | 12.9% por Folio / 82.6% híbrido | **CORRECTO** | $65.7M |
| **RIPLEY** | 100% rows / 100% $ | 0% | **FALSO POSITIVO MASIVO** | $413.9M |
| **FALABELLA** | 61.5% rows / 34.6% $ | 100% (4/4 XMLs) | **FALSO POSITIVO** | $2.6M |

### Hallazgo P0: Dashboard miente sobre certificación XML

El badge **"Verificado en SII/DTE"** (badge verde) usa `folio_xml IS NOT NULL` como condición. Pero `folio_xml` es el número de documento del XLSX fuente — NO una verificación contra SII.

Para RIPLEY (62,502 rows, $413.9M): **100% de las filas tienen badge verde "Verificado"** cuando en realidad **0% tiene respaldo DTE real.**

---

## P1: Provenance — Dashboard Display Fields

### Cadena completa: DB → API → Dashboard

```
                            SURGICAL_LOADER
                            ┌───────────────────────────────┐
                            │ Extrae folio_xml desde XLSX:  │
                            │ • ML:   "Factura Fiscal"      │
                            │ • PARIS: "Número factura"     │
                            │ • RIPLEY: "Núm. doc. liquidación" │
                            │ • FALABELLA: "N° Doc. Tributario" │
                            │ NO toca estado_xml            │
                            └──────────┬────────────────────┘
                                       │
                                       ▼
                            RUN_INITIAL_AUDIT
                            ┌───────────────────────────────┐
                            │ Solo legacy batch:            │
                            │ estado_xml = 'PENDIENTE'      │
                            │ (PARIS rows únicamente)       │
                            └──────────┬────────────────────┘
                                       │
                     ┌─────────────────┼─────────────────┐
                     │                 │                  │
                     ▼                 ▼                  ▼
              XML_MATCHER       XML_JUSTIFIER       MARKETPLACE_AUDITOR
         (monto+fecha ±7d)    (folio directo)      (classification)
         estado_xml='CERT'    estado_xml='CERT'    NO toca estado_xml
                     │        o 'SIN_RECURSO_XML'       │
                     └────────────┬─────────────────────┘
                                  │
                                  ▼
                          marketplace_ledger_v1
                    ┌──────────────────────────────┐
                    │  folio_xml (TEXT)            │ ← del loader
                    │  estado_xml (TEXT)           │ ← del matcher/justifier
                    │  asociacion_xml (TEXT)       │ ← del justifier
                    └──────────┬───────────────────┘
                               │
                               ▼
                       api/api.py (FastAPI port 8003)
                    ┌──────────────────────────────┐
                    │ GET /api/v4/ledger            │
                    │ SELECT * FROM                 │
                    │   marketplace_ledger_v1       │
                    │ Returns ALL columns.          │
                    │ NO transforma estado_xml.     │
                    └──────────┬───────────────────┘
                               │
                               ▼
                    templates/dashboard.html
                    ┌──────────────────────────────┐
                    │ JavaScript revisa:            │
                    │   if (row.folio_xml) {        │
                    │       badge = "Verificado"    │ ← VERDE, aunque sea XLSX sin SII
                    │       "Folio DTE: {folio}"    │
                    │   } else {                    │
                    │       badge = "Pendiente"     │ ← GRIS
                    │   }                           │
                    │ estado_xml NUNCA se consulta  │
                    └──────────────────────────────┘
```

### Mapeo exacto de términos

| Término Dashboard | Código Fuente | Columna DB | Realidad |
|---|---|---|---|
| **"Verificado en SII/DTE"** | `dashboard.html:568` | `folio_xml IS NOT NULL` | NO es verificación SII |
| **Badge verde con check** | `dashboard.html:580` | `folio_xml IS NOT NULL` | Es referencia del XLSX fuente |
| **"Folio DTE: {folio}"** | `dashboard.html:940` | `folio_xml` (texto plano) | Es el ID del documento fuente |
| **"Sin cruce en SII"** | `dashboard.html:944` | `folio_xml IS NULL` | Correcto — sin referencia |
| **estado_xml** | **NO se usa** | `estado_xml` | Columna huérfana en dashboard |

**Ni `folio_dte` ni `badge_dte` ni `estado_verificado` existen como columnas en la DB.** Son labels del dashboard derivados de `folio_xml`.

### Procesos que sí establecen estado_xml

| Proceso | estado_xml | ML | PARIS | RIPLEY | FALABELLA |
|---|---|---|---|---|---|
| **xml_matcher.py** (monto+fecha ±7d) | `'CERTIFICADO'` | SI | SI | NO | NO |
| **surgical_xml_justifier.py** (folio directo) | `'CERTIFICADO'` o `'SIN_RECURSO_XML'` | SI | SI | NO | NO |
| **run_initial_audit.py** (batch) | `'PENDIENTE'` | NO | SOLO PARIS | NO | NO |
| **surgical_loader.py** (nunca) | — | NO | NO | NO | NO |

---

## P2: Muestra 100 transacciones por Marketplace

### Metodología
- 100 filas aleatorias por marketplace (reservoir sampling, seed 42)
- Para cada fila: verificar `id_transaccion`, `fecha`, `detalle`, `monto`, `folio_xml`, `estado_xml`, `archivo_origen`
- Certificar cadena completa: Ledger Row → Campo fuente → XML asociado → Folio → Fecha → Monto

### ML — 100 transacciones

| Atributo | Resultado |
|---|---|
| Filas con folio_xml | 46/100 (46%) |
| Filas certificadas (estado_xml='CERTIFICADO') | 44/100 (44%) |
| Filas sin folio_xml (ajustes internos) | 54/100 (54%) |
| Archivo origen | `Reporte_Facturacion_*.xlsx` (Ventas/Comisiones) o `POS_*.xlsx` (Poscobro) |
| Cadena verificada | **SI** — folio_xml `033-0XXXXXXX` → XML en filesystem no encontrado por Folio directo (diferente formato), pero certificado por monto+fecha |

**Ejemplo certificado:**
```
Ledger:    SALE_2000013794009106_12_...xlsx
Campo:     Factura Fiscal (XLSX col)
folio_xml: 033-0010723408
estado:    CERTIFICADO (monto+fecha match)
Fecha:     2025-11-12
Monto:     $39,990
XML:       No encontrado por Folio directo (formato distinto)
```

### PARIS — 100 transacciones

| Atributo | Resultado |
|---|---|
| Filas con folio_xml | 13/100 (13%) |
| Filas con estado_xml='PENDIENTE' | 100/100 (100%) |
| Filas certificadas | **0/100 (0%)** — ninguna con CERTIFICADO |
| Archivo origen | XLSX con IDs numéricos (e.g., `13322861`) |
| Cadena verificada | **PARCIAL** — folio_xml poblado desde XLSX pero estado_xml='PENDIENTE' |

**Ejemplo:**
```
Ledger:    13322861
Campo:     Número factura (XLSX)
folio_xml: 24712148
estado:    PENDIENTE
Fecha:     2025-07-31
Monto:     $17,990
XML:       No hay puente por Folio directo confirmado
```

### RIPLEY — 100 transacciones

| Atributo | Resultado |
|---|---|
| Filas con folio_xml | **100/100 (100%)** |
| Filas certificadas | **0/100 (0%)** — todas NULL |
| estado_xml | **100% NULL** — ningún proceso ha corrido |
| Archivo origen | XLSX con IDs numéricos en `RIP_<folio>_` pattern |
| Cadena verificada | **NO** — folio_xml = "orden de pedido" (XLSX), NO DTE Folio |

**Ejemplo:**
```
Ledger:    RIP_556626_24219791201-A_comisionessobrepedidos
Campo:     Número documento liquidación (XLSX)
folio_xml: 556626
estado:    NULL
Fecha:     2025-12-06
Monto:     $-3,238
XML:       NO — bridge DTE inexistente
```

### FALABELLA — 100 transacciones

| Atributo | Resultado |
|---|---|
| Filas con folio_xml | 0/100 (0%) — 0 en muestra de 100 |
| Filas certificadas | **0/100 (0%)** |
| estado_xml | **100% NULL** |
| Archivo origen | UUIDs como id_transaccion (e.g., `e6d17494...`) |
| Cadena verificada | **NO** — sin estado_xml, sin relación XML en ledger |

---

## P3: XML → Ledger — Todos los XML del filesystem

### RIPLEY — 407 XMLs

| Atributo | Valor |
|---|---|
| Facturas (DTE 33) | 253 ($89.3M) |
| Liquidaciones (DTE 43) | 105 ($95.2M) |
| Guías (DTE 52) | 30 ($1.4M) |
| Notas Crédito (DTE 61) | 19 ($0.8M) |
| **Folios en ledger** | **0/407 (0%)** |
| **Monto representado** | **$0 / $186.7M (0%)** |
| **Exposición** | **$186.7M sin representación en ledger** |

### PARIS — 248 XMLs

| Atributo | Valor |
|---|---|
| Facturas (DTE 33) | 66 ($25.3M) |
| Liquidaciones (DTE 43) | 114 ($557.7M) |
| Notas Débito (DTE 56) | 17 ($7.3M) |
| Notas Crédito (DTE 61) | 51 ($226.3M) |
| **Folios en ledger** | **32/248 (12.9%)** |
| **Monto representado** | **$165.1M / $816.6M (20.2%)** |
| Nota | Matching híbrido: 82.6% monto cubierto por folio_xml (Sprint A2), pero solo 12.9% por Folio directo |

### FALABELLA — 4 XMLs

| Atributo | Valor |
|---|---|
| Facturas (DTE 33) | 2 ($1,642,247) |
| Notas Crédito (DTE 61) | 2 ($446,091) |
| **Folios en ledger** | **4/4 (100%)** |
| **Monto representado** | **$2,088,338 / $2,088,338 (100%)** |
| Nota | 100% de folios XML existen en ledger — pero solo 620/1,008 rows tienen folio_xml |

### ML — 186 XMLs

| Atributo | Valor |
|---|---|
| Facturas (DTE 33) | 30 ($109.1M) |
| Liquidaciones (DTE 43) | 89 ($134.9M) |
| Notas Débito (DTE 56) | 17 ($11.9M) |
| Notas Crédito (DTE 61) | 50 ($354.8M) |
| **Folios en ledger** | **0/186 (0%)** |
| **Monto representado** | **$0 / $610.7M (0%)** |
| Nota | Matching real: monto+fecha ±7d (xml_matcher.py). Folio XML (`033-XXXXXXXX`) NO corresponde a `<Folio>` del DTE (solo parte numérica) |

### Resumen P3

| Marketplace | XMLs | Folios en Ledger | Monto XML → Ledger | % |
|---|---|---|---|---|
| RIPLEY | 407 | 0/407 | $0 / $186.7M | **0.0%** |
| PARIS | 248 | 32/248 | $165.1M / $816.6M | **20.2%** |
| FALABELLA | 4 | 4/4 | $2.1M / $2.1M | **100.0%** |
| ML | 186 | 0/186 | $0 / $610.7M | **0.0%** |

**Nota crítica:** Los porcentajes por Folio directo son engañosos. ML y PARIS usan matching por monto+fecha, lo que produce certificación real aunque el Folio directo falle.

---

## P4: Inventario

### 4a. XML sin representación en Ledger (Folio no existe en ledger)

| Marketplace | XMLs sin Folio en Ledger | Monto no representado |
|---|---|---|
| RIPLEY | 407/407 | $186,705,151 |
| PARIS | 216/248 | $651,453,361 |
| FALABELLA | 0/4 | $0 |
| ML | 186/186 | $610,672,652 |
| **TOTAL** | **809/845** | **$1,448,831,164** |

**Aclaración:** Para ML y PARIS, la ausencia de Folio directo NO implica falta de certificación. ML tiene 88,323 rows ($522.6M) certificados por monto+fecha. PARIS tiene 100% estado_xml='PENDIENTE' pero matching híbrido parcial.

### 4b. Ledger sin representación XML

| Marketplace | Rows sin folio_xml | Monto sin folio_xml | Rows sin CERTIFICADO | Monto sin CERTIFICADO |
|---|---|---|---|---|
| RIPLEY | 0 | $0 | 62,502 | $413,893,686 |
| PARIS | 8,919 | $65,746,929 | 42,487 | $378,104,933 |
| FALABELLA | 388 | $3,464,631 | 1,008 | $2,583,016 |
| ML | 10,789 | $307,011,951 | 10,789 | $307,011,951 |
| **TOTAL** | **20,096** | **$376,223,511** | **116,786** | **$1,101,593,586** |

**Aclaración ML:** Los $307M sin folio_xml son conceptos de AJUSTE INTERNO (bpp_refunded, reconciled, etc.) que NO requieren XML. La exposición real de ML es $12.6M (SIN_RECURSO_XML).

### 4c. Duplicados en Ledger

| Marketplace | Grupos duplicados | Filas extra | Monto duplicado | Causa |
|---|---|---|---|---|
| **ML** | **0** | **0** | **$0** | Sin duplicados |
| **PARIS** | **0** | **0** | **$0** | Sin duplicados |
| **RIPLEY** | **0** | **0** | **$0** | Sin duplicados |
| **FALABELLA** | **125** | **883** | **$2,583,016** | id_transaccion UUID repetido (múltiples conceptos por transacción) |

**Análisis FALABELLA:** Los 125 `id_transaccion` duplicados NO son errores. `id_transaccion` usa el UUID de la transacción comercial, y una misma transacción puede tener múltiples movimientos (cargo por precio, comisión, envío, etc.). Son 125 transacciones con 883 movimientos totales. **No hay errores de duplicación real.**

### 4d. Duplicados en XML (filesystem)

| Marketplace | Folios duplicados | Causa |
|---|---|---|
| RIPLEY | 0 | Sin duplicados |
| PARIS | 0 | Sin duplicados |
| FALABELLA | 0 | Sin duplicados |
| ML | 0 | Sin duplicados |

**No hay XML duplicados en ningún marketplace.**

### 4e. Múltiples rows del ledger por mismo folio_xml

Es **estructural y esperado**: un solo documento tributario (factura) respalda múltiples transacciones.

| Marketplace | Ejemplo típico | Rows por folio | Conceptos distintos |
|---|---|---|---|
| ML | `033-0010723408` | 10,014 rows | 16 (Venta, Comisión, Envío, etc.) |
| PARIS | `23980722` | 3,950 rows | 5 (Venta, Devolución, Despacho, etc.) |
| RIPLEY | `517031` | 3,382 rows | 11 (Importe, Comisión, Envío, etc.) |
| FALABELLA | `460690` | 365 rows | 5 (Precio, Comisión, Envío, etc.) |

Este es el **patrón esperado**: 1 XML (factura del período) respalda N transacciones del ledger.

---

## P5: Exposición Económica

### 5a. Monto XML sin representación en Ledger

| Marketplace | Monto XML Total | Monto XML representado | **XML sin Ledger** | % No Representado |
|---|---|---|---|---|
| RIPLEY | $186,705,151 | $0 | **$186,705,151** | 100.0% |
| PARIS | $816,572,627 | $165,119,266 | **$651,453,361** | 79.8% |
| FALABELLA | $2,088,338 | $2,088,338 | **$0** | 0.0% |
| ML | $610,672,652 | $0 | **$610,672,652** | 100.0% |
| **TOTAL** | **$1,616,038,768** | **$167,207,604** | **$1,448,831,164** | **89.7%** |

### 5b. Monto Ledger sin representación XML

| Marketplace | Ledger Total | No CERTIFICADO | Real sin cobertura | Nota |
|---|---|---|---|---|
| RIPLEY | $413,893,686 | $413,893,686 | **$413,893,686** | 100% sin certificar |
| PARIS | $378,104,933 | $378,104,933 | **$65,746,929** (sin folio) | 100% PENDIENTE (estado_xml existe) |
| FALABELLA | $2,583,016 | $2,583,016 | **$2,583,016** | 100% NULL |
| ML | $842,250,301 | $319,653,882 | **$12,641,931** (SIN_RECURSO_XML) | $307M = ajustes (NO requieren XML) |
| **TOTAL** | **$1,636,831,936** | **$1,114,235,517** | **$494,865,562** | |

### 5c. Exposición Neta Real

Considerando solo conceptos que REQUIEREN XML (excluyendo ajustes internos, settlement, promocionales):

| Marketplace | Exposición Bruta | Ajustes/Settlement | **Exposición Real** | Riesgo |
|---|---|---|---|---|
| RIPLEY | $413,893,686 | -$206,946,843 (A pagar) | **$206,946,843** | **CRITICO** |
| PARIS | $378,104,933 | -$1,344,641 (ajustes) | **$376,760,292** | BAJO (100% PENDIENTE) |
| FALABELLA | $2,583,016 | -$840 (ajuste) | **$2,582,176** | **CRITICO** |
| ML | $319,653,882 | -$307,011,951 (ajustes) | **$12,641,931** | BAJO |
| **TOTAL** | **$1,114,235,517** | **-$515,304,275** | **$598,931,242** | |

---

## Hallazgos Clave

### H1: Badge DTE es engañoso para 3/4 marketplaces

El dashboard muestra "Verificado en SII/DTE" cuando `folio_xml IS NOT NULL`. Pero:

| Marketplace | Rows con badge verde | Realmente verificado vs SII |
|---|---|---|
| **RIPLEY** | **62,502 ($413.9M)** | **0** — folio_xml = orden de pedido XLSX |
| **PARIS** | **33,568 ($312.4M)** | **Parcial** — matching híbrido, estado PENDIENTE |
| **FALABELLA** | **620 ($0.9M)** | **0** — solo folio_xml desde XLSX |
| **ML** | **90,814 ($535.2M)** | **Sí** — certificado por monto+fecha |

**Impacto:** 96,690 rows ($415.2M) muestran badge verde "Verificado" sin certificación real.

### H2: estado_xml es columna huérfana en el dashboard

`estado_xml` está poblada en ML (89.4% rows) y PARIS (100%), pero el dashboard **nunca la consulta**. El badge se determina exclusivamente por `folio_xml`.

### H3: Matching por Folio directo solo funciona en FALABELLA (4/4)

| Marketplace | Método de certificación real |
|---|---|
| **ML** | **Monto+fecha ±7 días** (xml_matcher.py) — 88,323 rows certificadas |
| **PARIS** | **Híbrido**: monto+fecha + Folio (Sprint A2) — 33,568 rows con folio_xml |
| **RIPLEY** | **NINGUNO** — 0 rows certificadas. 407 XMLs sin puente |
| **FALABELLA** | **Folio directo** (4/4 XMLs) pero solo 620/1,008 rows tienen folio |

### H4: Duplicación cero en ledger (intencional)

No hay `id_transaccion` duplicados en ML, PARIS, ni RIPLEY. Los 125 "duplicados" en FALABELLA son el patrón esperado (1 transacción → múltiples conceptos).

### H5: No hay XML duplicados en filesystem

845 XMLs totales, 0 folios duplicados. Integridad documental OK.

### H6: El mayor gap no es por monto sino por certificación

La exposición nominal de **$1,114M** se reduce a **$599M** al excluir ajustes/settlement. Pero aún así:

- **RIPLEY ($207M)**: requiere reconstruir puente desde cero (monto+fecha)
- **PARIS ($377M)**: tiene 100% estado_xml=PENDIENTE — el gap es de matching, no de documentos
- **ML ($12.6M)**: residual — 2,491 rows SIN_RECURSO_XML
- **FALABELLA ($2.6M)**: no hay DTEIndexer ejecutado

---

## Resumen de Brechas

| Brecha | Descripción | Impacto | Prioridad |
|---|---|---|---|
| **G1** | Dashboard badge "Verificado" muestra falso positivo para RIPLEY/FALABELLA | 96,690 rows, $415.2M | **P1** |
| **G2** | RIPLEY: 0% certificación XML ($207M P&L sin soporte) | Riesgo auditoría SII | **P0** |
| **G3** | FALABELLA: 0% estado_xml, 100% NULL | Sin trazabilidad | **P1** |
| **G4** | estado_xml no se usa en dashboard | Columna huérfana | **P2** |
| **G5** | ML/PARIS: Folio directo = 0% match (XML `<Folio>` vs ledger `folio_xml`) | Matching estructural | **P2** |

---

## Verificación de Completitud

### Ledger → XML (¿Cada transacción tiene su XML?)

| Marketplace | % con folio_xml | % certificado | **Completitud** |
|---|---|---|---|
| RIPLEY | 100% | 0% | **CRITICO** |
| PARIS | 79.0% | 0% (PENDIENTE) | **PARCIAL** |
| FALABELLA | 61.5% | 0% | **CRITICO** |
| ML | 89.4% | 89.4% | **CERTIFICADO** |

### XML → Ledger (¿Cada XML respalda transacciones?)

| Marketplace | % Folios en Ledger | % Monto representado | **Completitud** |
|---|---|---|---|
| RIPLEY | 0% | 0% | **CRITICO** |
| PARIS | 12.9% | 20.2% | **PARCIAL** |
| FALABELLA | 100% | 100% | **CERTIFICADO** |
| ML | 0% | 0% | **PARCIAL** (monto+fecha funciona) |

### Bidireccional

| Marketplace | Ledger → XML | XML → Ledger | **Certificación** |
|---|---|---|---|
| RIPLEY | CRITICO | CRITICO | **NO CERTIFICADO** |
| PARIS | PARCIAL | PARCIAL | **NO CERTIFICADO** |
| FALABELLA | CRITICO | CERTIFICADO | **NO CERTIFICADO** |
| ML | CERTIFICADO | PARCIAL | **NO CERTIFICADO (formalmente)** |

---

## Conclusión

**Ningún marketplace tiene completitud bidireccional certificada.**

- **ML** es el más cercano: 89.4% rows con estado_xml=CERTIFICADO. Pero 0% de los XMLs del filesystem se vinculan por Folio directo al ledger. La certificación existe por monto+fecha, un método indirecto.
- **PARIS** tiene 100% estado_xml poblado (PENDIENTE) y 82.6% folio_xml, pero el matching formal (Sprint A2) usó columnas puente no documentadas del XLSX.
- **RIPLEY** es la brecha más grande: $207M P&L sin ningún XML vinculado. 407 XMLs existen pero 0% linkage.
- **FALABELLA** tiene 100% match por Folio (4/4 XMLs) pero el DTEIndexer nunca se ejecutó y el ledger tiene 0% estado_xml.
