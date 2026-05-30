RFC-PARIS-XML-TRACEABILITY
===========================
Fecha: 2026-05-29
Estado: PROPUESTA (NO IMPLEMENTADA)
Tipo: Deuda técnica controlada
Prioridad: MEDIA
Requiere: Snapshot V7 post-implementación
No altera: BASELINE_ESTABLE_V6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. OBJETIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Propagar dos campos desde el loader PARIS hasta el ledger:

  numero_factura       →  folio_xml (columna existente)
  nro_solicitud_factura → nueva columna solicitud_xml (a crear)

Sin alterar BASELINE_V6. Sin rebuild global.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. EVIDENCIA DOCUMENTAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Caso verificado en forense exacto (2026-05-29):

  2.1 Archivo XML
  ────────────────
  Física:   01_Raw/PARIS/Facturacion/dteproveedor_5088.xml
  Emisor:   CENCOSUD Retail S.A. (RUT 81201000-K)
  Tipo DTE: 33 (Factura Electrónica)
  Folio:    22031868
  FolioRef: 742794668
  Monto:    $61,001
  Fecha:    2024-10-28

  2.2 Excel PARIS
  ───────────────
  Archivo:  Transacciones/Fulfillment/1 ene 2024 - 31 dic 2024.xlsx
  Columna "número factura":       22031868 (59 filas, rows 3176-3298)
  Columna "nro solicitud factura": 742794668 (mismas 59 filas)
  Ambas columnas en las MISMAS filas → relación 1:1

  2.3 Ledger
  ──────────
  marketplace_ledger_v1 WHERE marketplace='PARIS':
    42,487 rows, 0 con folio_xml no-nulo
    22031868: NO ENCONTRADO en id_transaccion, folio_xml, ni id_orden
    742794668: NO ENCONTRADO en ninguna columna

  2.4 Cadena
  ───────────
  XML <Folio>         (22031868)  ──┐
  XML <FolioRef>      (742794668) ──┤
                                    │
  Excel "número factura"     ───────┤
  Excel "nro solicitud factura" ────┤
                                    │
  Ledger folio_xml                 ──┘  ← RUPTURA AQUÍ
  Ledger (nueva columna)           ──┘  ← NI EXISTE

  La ruptura está en EXCEL → LEDGER, no en XML → EXCEL.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. ESTADO ACTUAL POR MARKETPLACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ML:       FULL    — 89.4% ledger con folio_xml, 762 XML indexados
  PARIS:    PARTIAL — Folio XML = Excel "número factura" (T33),
                      pero 0% propagado a ledger.
                      Folio XML ≠ Excel para T43.
  RIPLEY:   NONE    — Sin columna "Documento Tributario" en Excel.
                      269,216 rows sin folio_xml.
  FALABELLA: NONE   — 620 rows con folio_xml pero son IDs internos,
                      no folios DTE. 4 XMLs no indexados.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. CAMBIOS REQUERIDOS (PARA IMPLEMENTACIÓN FUTURA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  4.1 surgical_loader.py — Carga PARIS (líneas ~305-340)
  ────────────────────────────────────────────────────────
  Actual:
    c_folio = get_col_name(df, ['número factura', 'factura'])
    ...
    folio = str(row[c_folio]) if c_folio and pd.notna(row[c_folio]) and ...

  Cambio:
    c_folio = get_col_name(df, ['número factura', 'factura'])
    c_solicitud = get_col_name(df, ['nro solicitud factura', 'solicitud factura', 'solicitud liq.factura'])
    ...
    folio = str(row[c_folio]) if c_folio and pd.notna(row[c_folio]) and ...
    solicitud = str(row[c_solicitud]) if c_solicitud and pd.notna(row[c_solicitud]) and ...

  4.2 surgical_loader.py — LEDGER_COLS + dict del ledger
  ────────────────────────────────────────────────────────
  Actual:
    LEDGER_COLS = ['marketplace', 'id_transaccion', 'id_orden', 'fecha',
                   'detalle', 'monto', 'tipo_movimiento', 'archivo_origen',
                   'folio_xml']

  Cambio:
    Agregar 'solicitud_xml' a LEDGER_COLS.
    Agregar 'solicitud_xml': solicitud al dict del ledger.

  4.3 marketplace_auditor.py — Si aplica (opcional)
  ─────────────────────────────────────────────────────
  Si folio_xml ya existe en el ledger post-carga, no requiere cambios.
  Si se requiere indexar PARIS XML en dte_truth_v1:
    - Crear _reload_dte_truth_paris.py (similar a _reload_dte_truth.py)
    - Indexar por RUT emisor 81201000-K + Folio

  4.4 DB schema
  ─────────────────
  ALTER TABLE marketplace_ledger_v1 
    ADD COLUMN solicitud_xml VARCHAR;

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. RIESGOS Y RESTRICCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  5.1 PARIS tiene DOS tipos de DTE:
    - Tipo 33 (Factura Electrónica): Folio en XML = "número factura" en Excel ✓
    - Tipo 43 (Liquidación-Factura): Folio en XML ≠ "número factura" en Excel ✗
    - Ejemplo: Folio 14629 (T43) NO está en Excel
    - La propagación solo funciona para T33. T43 requiere otro approach.

  5.2 "número factura" NO es único por transacción:
    - Es el mismo para TODAS las filas de un batch de liquidación.
    - 59 filas comparten 22031868.
    - Útil para cruce agregado, no para reconciliación 1:1.

  5.3 RIPLEY requiere su propio RFC:
    - Sin columna "Documento Tributario" → necesita mapeo diferente.
    - "Número documento liquidación" (500346, 503106, ...) NO coincide con
      Folios XML (14042-53136439).

  5.4 FALABELLA:
    - Los folios_xml existentes (401935, 404621, ...) son IDs de órdenes,
      NO folios DTE. No hay XML físico vinculable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. PLAN DE IMPLEMENTACIÓN SUGERIDO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Fase 1 — PARIS folio_xml (surgical_loader.py solo)
    1. Agregar c_solicitud + extracción de solicitud_xml
    2. Agregar solicitud_xml a LEDGER_COLS
    3. Recargar solo archivos PARIS (vaciado de dominio controlado)
    4. Validar: SQL SUM pre = SQL SUM post, DIFF 0
    5. Generar snapshot V7

  Fase 2 — Indexar XML PARIS en dte_truth_v1 (opcional)
    1. Crear _reload_dte_truth_paris.py
    2. Indexar por RUT emisor 81201000-K
    3. Validar cruce folio_xml ↔ dte_truth para T33

  Fase 3 — RIPLEY (RFC separado)
    1. Investigar columna "Número documento liquidación"
    2. Determinar si existe relación con XML
    3. RFC independiente si procede

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. APROBACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Estado: PROPUESTA — pendiente de autorización para implementar.
  Implementación requiere:
    - Aprobación explícita
    - Snapshot de seguridad pre-cambio
    - Test de regresión completo (14/14)
    - Nuevo snapshot V7 post-cambio

  NO IMPLEMENTAR sin autorización.
  NO ALTERAR BASELINE_V6.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. REFERENCIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - FORENSIC_XML_SUMMARY.md (hallazgos actualizados 2026-05-29)
  - _forense_exact_match.py (búsqueda exacta por identificador)
  - _forense_final_chain.py (cadena completa verificado)
  - _forense_check_xml_folios.py (verificación XML → Excel)
  - governance/FREEZE_ACTIVO.txt (V6, reglas de cambio)
  - governance/CHANGE_TEMPLATE.txt (template obligatorio)
