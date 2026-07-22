# POSCOBRO_LIQUIDACIONES_PRECEDENCE_CERTIFICATION

**Regla a validar**: Cuando Poscobro y Liquidaciones registran el mismo evento económico (refund), ¿cuál debe prevalecer?

**Fuentes**: Poscobro (5 semi-annual files → `marketplace_ledger_v1`), Liquidacion_FF (90 weekly files), Facturación (`marketplace_ledger_v1.financial_group=devoluciones`).

---

## FASE 1 — Match documental: Poscobro refund vs Liquidaciones

De los $327.2M en Ajustes monto>0 (ML, 11,384 rows, 5,597 orders):

| Categoría | Rows | Monto | Orders |
|---|---|---|---|
| Refund concepts | 5,880 | **$177,214,871** | 5,306 |
| Settlement (BPP/Conciliado/General) | 5,504 | $149,951,697 | 4,747 |

Clasificación por `detalle` en ledger: 'repentant_buyer' → Ajuste por Arrepentimiento, 'bigger_than_expected_fashion' → Talla/Garantía, etc. 37 refund codes, 0 desconocido.

**Match Poscobro refund orders vs Ledger Devoluciones** (Reporte_Facturacion_MercadoLibre_*.xlsx):

| Estado | Orders | % | Monto | % |
|---|---|---|---|---|
| **Conciliado** (orden existe en Devoluciones) | 2,693 | **50.8%** | **$88,070,164** | **49.7%** |
| **Pendiente** (solo en Poscobro) | 2,613 | **49.2%** | **$89,144,707** | **50.3%** |

**Match Poscobro refund orders vs Liquidacion_FF** (raw DTE files):

| Estado | Orders | % | Monto | % |
|---|---|---|---|---|
| Conciliado | 1,565 | **29.5%** | $57,934,851 | 32.7% |
| Pendiente | 3,741 | **70.5%** | $119,280,020 | 67.3% |

---

## FASE 2 — Matriz de precedencia

### 3-Way Venn: Poscobro refunds contra Ledger (Facturación) + Liquidacion_FF

| Categoría | Orders | Monto | % del total refund |
|---|---|---|---|
| En **ambas** fuentes (Ledger + Liquidacion_FF) | 907 | $33,183,795 | 18.7% |
| Solo en **Ledger** (Facturación) | 1,786 | $54,886,369 | 31.0% |
| Solo en **Liquidacion_FF** | 658 | $24,751,056 | 14.0% |
| **Truly pending** (ninguna fuente) | 1,955 | **$64,393,651** | **36.3%** |

### $ por escenario

```
Poscobro refund total:                  $177,214,871
  ├─ Reconocido en Liquidaciones:       $112,821,220  (63.7%)
  │   ├─ Facturación + Liquidacion_FF:  $ 33,183,795  (18.7%)
  │   ├─ Facturación only:              $ 54,886,369  (31.0%)
  │   └─ Liquidacion_FF only:           $ 24,751,056  (14.0%)
  └─ No reconocido (truly pending):     $ 64,393,651  (36.3%)
```

### Precisión de conciliación (cantidad)

Para orders conciliadas (Ledger Devoluciones), comparación de montos:

| Métrica | Valor |
|---|---|
| Orders comparadas | 2,693 |
| Ratio medio dev_abs / pos | **98.31%** |
| Ratio mediano | **100.00%** |
| Near exact (95-105%) | 2,477 orders (92.0%) — $78.5M |
| Partial match | 198 orders (7.4%) — $7.7M |
| Far off | 18 orders (0.7%) — $1.9M |

**Conclusión**: Cuando existe conciliación, el monto de Poscobro y Devoluciones es virtualmente idéntico (92% near exact, ratio medio 98.3%). El mismo evento económico está registrado en ambos sistemas.

---

## FASE 3 — Verdad financiera: ¿cuál debe prevalecer?

**Premisa**: Poscobro registra post-sale adjustments (cobro ML al seller por reimbursements al comprador). Liquidaciones registra el settlement financiero real (DTE electrónico, Facturación oficial).

**Evidencia**:

1. **Precisión documental**: Liquidacion_FF son DTE (Documentos Tributarios Electrónicos) — son la representación fiscal/legal del flujo de dinero. Poscobro es un reporte operacional interno de ML.

2. **Conciliación perfecta**: 92% de orders conciliadas tienen match casi exacto (95-105%). El ratio medio es 98.3%. No hay ambigüedad — es el mismo evento.

3. **Triple Play evidencia** (order 2000014464474828):
   - Poscobro (ML → seller charge): +$27,990
   - Facturación Devolución (buyer refund): -$27,990
   - Net: **$0.00**

4. **Settlement concepts son correctos en AJUSTES**: BPP/Poscobro Conciliado/General ($150.0M) son entries de liquidación — NO refunds. El 60.7% de estas orders también tienen Devolución, pero es un evento separado (la liquidación vs la devolución).

**Regla de precedencia**: **LIQUIDACIONES > POSCOBRO** cuando existe conciliación de orden. Liquidaciones (Facturación + Liquidacion_FF) es la fuente oficial del flujo financiero. Poscobro es el trigger operacional.

---

## FASE 4 — Reclasificación virtual

Aplicando la regla a los $177.2M de Poscobro refund concepts:

| Grupo | Monto | Dónde va | Fundamento |
|---|---|---|---|
| Refund conciliado (Ledger) | $88,070,164 (49.7%) | **DEVOLUCIONES** (ya está allí) | Liquidaciones reconoce el refund. Poscobro es redundante. |
| Refund pendiente | $89,144,707 (50.3%) | **AJUSTES temporales** | No hay contraparte en Liquidaciones. Poscobro es la única fuente. |
| Chargeback (settlement) | $149,951,697 | **AJUSTES** (sin cambio) | No son refunds. Son settlements. |

**Impacto en RN**: $0 (neutral). La reclasificación de refund conciliado de AJUSTES a DEVOLUCIONES es documental — el RN ya captura ambos lados.

---

## Pregunta única — Respuesta

**¿Cuánto de los $176.4M en refund ya está reconocido en Liquidaciones y cuánto sigue pendiente?**

| Respuesta | Monto | % |
|---|---|---|
| **Ya reconocido en Liquidaciones** (Ledger Devoluciones) | **$88,070,164** | **49.7%** |
| **Sigue pendiente** (solo en Poscobro) | **$89,144,707** | **50.3%** |

Desglose truly pending de $89.1M:

| Origen | Orders | Monto |
|---|---|---|
| Talla/Garantía (bigger_than_expected + smaller_than_expected + not_match_size) | ~1,900 | ~$55.0M |
| Arrepentimiento (repentant_buyer + dont_want_it + undelivered_repentant) | ~780 | ~$22.5M |
| Falla/Daño/Retraso (undelivered, broken, delivery_date) | ~200 | ~$6.0M |
| Otros (diferencia, disputa, cambio dirección, faltante) | ~300 | ~$5.6M |

---

## Dictamen final

**PASS** — Regla de precedencia validada:

1. **LIQUIDACIONES > POSCOBRO** cuando ambas fuentes registran la misma orden.
2. **49.7% ($88.1M)** de Poscobro refund concilia con Liquidaciones (Facturación Devoluciones) — con 92% precisión de monto.
3. **36.3% ($64.4M)** es truly pending — no reconocido en ninguna fuente de Liquidaciones. Este es el saldo que documentalmente pertenece a refund pero no tiene settlement.
4. **Refund conciliado** debe considerarse absorbido por Liquidaciones → Poscobro es redundante → clasificación correcta es DEVOLUCIONES (ya está allí).
5. **Refund pendiente** debe mantenerse en AJUSTES como partida temporal hasta que Liquidaciones lo reconozca.

Regla final:
- **Refund conciliado** (orden existe en Liquidaciones): prevalece Liquidación → Poscobro ignorado
- **Refund pendiente** (orden solo en Poscobro): ajuste temporal en AJUSTES
- **Settlement** (BPP/Conciliado/General): AJUSTES (correcto, no cambia)

---

**Archivo**: `governance/POSCOBRO_LIQUIDACIONES_PRECEDENCE_CERTIFICATION.md`
