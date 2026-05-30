FORENSE RIPLEY — MATRIZ COMPLETA XML → EXCEL → LEDGER
=======================================================
Fecha: 2026-05-29
Estado: SOLO DIAGNÓSTICO — NO IMPLEMENTAR

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. INVENTARIO XML RIPLEY — CAMPOS RELEVANTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Archivos: 196 XML en 01_Raw/RIPLEY/Documentos Recepcionados/
Esquema: SII EnvioDTE (Chile), emisor CENCOSUD
Encoding: ISO-8859-1

CAMPO XML                  TIPO          VALORES EJEMPLO
────────────────────────────────────────────────────────────────
<Folio>                    int (196 uniq) 14629, 121151, 53136430
<FolioRef>                 int (51 uniq)  735105591, 726467343
<TipoDTE>                  int (4 uniq)   33, 43, 52
<TpoDTE>                   int (4 uniq)   33, 43, 52 (subtotales)
<RUTEmisor>                RUT (2 uniq)   81201000-K, 83382700-6
<RznSoc>                   str (4 uniq)   CENCOSUD RETAIL S.A.
<RUTRecep>                 RUT (1 uniq)   77898100-9
<FchEmis>                  date (98 uniq) 2024-10-02 .. 2026-04-30
<MntTotal>                 int (185 uniq) 48800, 39980, 5186615
<MntNeto>                  int (183 uniq)
<IVA>                      int (183 uniq)
<TasaIVA>                  dec (3 uniq)   19, 19.0, 19.00
<ValComNeto>               int (70 uniq)  Comisión neta
<ValComIVA>                int (70 uniq)  IVA comisión
<CdgIntRecep>              str (2 uniq)   4200000519, 778981009
<CdgVendedor>              str (4 uniq)   Código vendedor
<Contacto>                 str (1 uniq)   956980667
<DirOrigen>                str (6 uniq)   Dirección emisor
<DirRecep>                 str (4 uniq)   Dirección receptor
<Detalle><NmbItem>         str (331 uniq) Nombre producto
<Detalle><MontoItem>       int (436 uniq) Monto ítem
<Detalle><PrcItem>         int (386 uniq) Precio ítem
<Detalle><QtyItem>         int (91 uniq)  Cantidad
<Detalle><VlrCodigo>       str (157 uniq) SKU / código interno
<Signature>                varios         Firma electrónica (no datos)

Documento ID (atributo):   str (118 uniq) T33F22031868, etc.
Liquidacion ID (atributo): str (78 uniq)  S20241029T043F0000014629
SetDTE ID (atributo):      str (196 uniq) EnvioDTE-81201000-K-...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. INVENTARIO EXCEL RIPLEY — COLUMNAS (40 archivos)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ubicación: 01_Raw/RIPLEY/ (000312-2815.xlsx ... 000371-2815.xlsx)
Columnas detectadas: 37 únicas (normalizadas)

NORMALIZED NAME          ORIGINAL NAME           TIPO DATOS
────────────────────────────────────────────────────────────────
1.  fechaoc               Fecha OC               date (dd-mm-yyyy)
2.  numerodocumentoliquidacion  Número documento liquidación  int (1/file, secuencial ~500K)
3.  ordendecompra         Orden de compra         str (#-A)
4.  shopid                Shop ID                int (2815 constante)
5.  tienda                Tienda                 str (NICOPOLY, etc.)

6.  importedelpedido      Importe del pedido     int (bruto venta)
7.  envio                 Envío                  int
8.  gastosdeenviopagadosporeloperador  Gastos de envío pagados por el operador  int
9.  comisionessobrepedidos  Comisiones sobre pedidos  int
10. pedidosreembolsados   Pedidos reembolsados   int
11. envioreembolsado      Envío reembolsado      int
12. gastosdeenvioreembolsadospagadosporeloperador  Gastos de envío reembolsados...  int
13. comisionessobrepedidosreembolsados  Comisiones sobre pedidos reembolsados  int
14. abonopostventa        Abono postventa        int
15. abonoporerrordecomision  Abono por error de comisión  int
16. abonoextraordinarioerrordeprecio  Abono extraordinario - error de precio  int
17. abonoofertatcopex     Abono oferta TC - OPEX  int
18. abonoporusodeflotapropia  Abono por uso de flota propia  int
19. otrosabonos           Otros abonos           int
20. abonossolucionescomerciales  Abonos soluciones comerciales  int
21. abonosporcuponpromocional  Abonos por cupón promocional  int
22. descuentoofertatcopex Descuento oferta TC - OPEX  int
23. otrosdescuentos       Otros descuentos       int
24. descuentoporerrordeclaselogistica  Descuento por error de clase logistica  int
25. descuentoporcostologistico  Descuento por costo logístico  int
26. descuentoporlogisticainversa  Descuento por logistica inversa  int
27. descuentoporcancelacion  Descuento por cancelación  int
28. descuentoporcompensacionacliente  Descuento por compensación a cliente  int
29. descuentoffsobreestadia  Descuento FF - sobreestadía  int
30. descuentoffpickandpack  Descuento FF - pick and pack  int
31. descuentoffotros      Descuento FF - Otros   int
32. descuentoporpdm       Descuento por PDM      int
33. cobrodespachoprimeramilla  Cobro despacho primera milla  int
34. descuentooperacional  Descuento operacional   int
35. abonoporformalizacionaopl  Abono por formalización a OPL  int
36. descuentoporcuponesdedespacho  Descuento por cupones de despacho  int
37. apagar                A pagar                 int (neto final)

Total columnas en Excel: 37
Columnas financieras: 29 (ítems 6–37)
Columnas estructurales: 5 (ítems 1–5, fechaoc + liq + orden + shop + tienda)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. INVENTARIO LEDGER RIPLEY — COLUMNAS CARGADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tabla: marketplace_ledger_v1 (15 columnas)
Filas RIPLEY: 269,216

COLUMNA                  ORIGEN EXCEL              VALORES
────────────────────────────────────────────────────────────────
marketplace              fijo "RIPLEY"             "RIPLEY"
id_transaccion           construido: "RIP_{liq}_{orden}_{detalle}"
id_orden                 Orden de compra           "23246187401-A"
fecha                    Fecha OC                  date
detalle                  nombre columna financiera "Importe del pedido"
monto                    valor columna financiera  int/float
tipo_movimiento          según detalle             "PAGO"/"CARGO"
archivo_origen           filename                  "000312-2815.xlsx"
folio_xml                Número documento liq.     NULL (no poblado por código anterior)
estado_xml               (sin origen)              NULL
load_ts                  automático                timestamp
asociacion_xml           (sin origen)              NULL
financial_group          (asignado por auditor)    valor
clasificacion_operativa  (asignado por auditor)    valor
include_in_operational_pnl (asignado por auditor)  true/false

Columnas de origen Excel PERSISTENTES en ledger:
  - Fecha OC → fecha ✓
  - Orden de compra → id_orden ✓
  - Número documento liquidación → folio_xml ✓ (code extracts, DB tiene NULL por carga antigua)
  - 29 columnas financieras → detalle + monto (vía melt) ✓

Columnas DESCARTADAS por ETL:
  - Shop ID           L387: excluded from value_vars (hardcoded)
  - Tienda            L387: excluded from value_vars (hardcoded)

Estas 2 columnas existen en Excel pero NO llegan al ledger.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. MATRIZ CAMPO → ORIGEN → DESTINO → PERSISTE / SE PIERDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMATO:
CAMPO_XML | ORIGEN | ORIGEN_EXCEL | DESTINO_LEDGER | ESTADO | UBICACIÓN | NOTA

F = PERSISTE (FULL)
P = PERSISTE PARCIAL
X = SE PIERDE (NO SOPORTADO)
E = EXISTE EN CÓDIGO PERO DB NO POBLADA

CAMPO XML              ORIG_EXCEL?   DESTINO LEDGER     ESTADO  UBICACIÓN
─────────────────────────────────────────────────────────────────────────
<Folio>                NO            —                    X      XML→Excel se rompe
<FolioRef>             NO            —                    X      XML→Excel se rompe
<TipoDTE>              NO            —                    X      XML→Excel se rompe
<RUTEmisor>            NO            —                    X      XML→Excel se rompe
<RznSoc>               NO            —                    X      XML→Excel se rompe
<RUTRecep>             NO            —                    X      XML→Excel se rompe
<FchEmis>              Fecha OC      fecha                P      Fecha OC ≠ FchEmis (son distintas)
<MntTotal>             NO            —                    X      XML→Excel se rompe
<MntNeto>              NO            —                    X      XML→Excel se rompe
<IVA>                  NO            —                    X      XML→Excel se rompe
<ValComNeto>           Comisiones s/pedidos  detalle+monto F      PERSISTE en melt
<ValComIVA>            (en Comisiones)       detalle+monto F      PERSISTE (incluido)
<CdgIntRecep>          NO            —                    X      XML→Excel se rompe
<CdgVendedor>          NO            —                    X      XML→Excel se rompe
<Detalle><NmbItem>     NO            —                    X      Solo agregados, no ítems
<Detalle><MontoItem>   NO            —                    X      Solo agregados
<Detalle><PrcItem>     NO            —                    X      Solo agregados
<Detalle><QtyItem>     NO            —                    X      Solo agregados
<Detalle><VlrCodigo>   NO            —                    X      Solo agregados

CAMPO EXCEL            DESTINO LEDGER                   ESTADO  UBICACIÓN
─────────────────────────────────────────────────────────────────────────
Número documento liq.  folio_xml                         E      surgical_loader.py L411 (code OK, DB NULL)
Orden de compra        id_orden                          F      surgical_loader.py L408
Fecha OC               fecha                             F      surgical_loader.py L408
Shop ID                — (descartado)                    X      surgical_loader.py L387
Tienda                 — (descartado)                    X      surgical_loader.py L387
29 cols financieras    detalle + monto (melt)            F      surgical_loader.py L388-392

CAMPO LEDGER           ORIGEN                           ESTADO
─────────────────────────────────────────────────────────────────────────
folio_xml              Número documento liquidación      E (code ok, DB null)
id_orden               Orden de compra                   F
fecha                  Fecha OC                          F
detalle                29 cols financieras                F (melt)
monto                  valor de cada columna              F (melt)

RESUMEN DE PÉRDIDA:
  XML → Excel: 17 campos XML NO TIENEN CORRESPONDENCIA en ninguna columna Excel
  Excel → Ledger: 2 campos Excel (Shop ID, Tienda) DESCARTADOS en L387
  Ledger → DB: 1 campo (folio_xml) EXTRAÍDO por código pero NULL en DB (carga antigua)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. VEREDICTO: NONE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RIPLEY = NONE para trazabilidad XML.

Razones:

1.  196 XMLs Folio (14629..53136439) → NO aparece en ninguna columna Excel.
    El Excel usa Número documento liquidación (~500K, secuencial propio).

2.  51 XMLs FolioRef (735105591..) → NO aparece en ninguna columna Excel.

3.  3 tipos DTE (33/43/52) → NO hay columna Tipo DTE en Excel.

4.  4 razones sociales emisor → NO hay columna RUT Emisor en Excel.
    (Tienda solo tiene "NICOPOLY" etc., no RUT.)

5.  Las únicas columnas compartibles entre XML y Excel son montos financieros,
    pero estos son genéricos (comisiones, descuentos) y no identifican un DTE único.

6.  Número documento liquidación (Excel, 500346..579224) SÍ llega a folio_xml
    (por código, pero DB no poblada). Aun así: NO ES FOLIO DTE. Son IDs de
    liquidación internos de CENCOSUD, no folios SII.

DIFERENCIA CRÍTICA CON PARIS:
  PARIS: XML <Folio> = Excel "número factura" → cadena PARCIAL verificada.
  RIPLEY: No existe ninguna columna Excel que contenga valores de Folio XML.
          No hay cadena que conectar, ni siquiera parcial.

LA RECONCILIACIÓN INDIVIDUAL POR FOLIO DTE
NO ES POSIBLE PARA RIPLEY
CON LOS DATOS ACTUALES.

No hay columna puente.
No hay overlap numérico.
No hay overlap semántico.

LOS SISTEMAS SON INCONEXOS.
