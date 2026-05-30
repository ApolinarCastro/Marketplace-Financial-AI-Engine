"use strict";

// ───────────────────────────────────────────────────────────
//  Integración del MASTER_MARKETPLACE_DICTIONARY_V1 en los
//  módulos engine/v4/marketplace_auditor.py y surgical_loader.py
// ───────────────────────────────────────────────────────────

import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const ROOT = "C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine";

async function main() {
  // 1. Leer el dictionary desde el JSON que nos pasó el usuario
  //    (lo tenemos como literal en el prompt — lo escribimos a disco)

  const dict = {
    dictionary_name: "MASTER_MARKETPLACE_DICTIONARY_V1",
    version: "1.0",
    scope: {
      included_marketplaces: ["MERCADO_LIBRE", "RIPLEY", "PARIS", "FALABELLA"],
      excluded: ["SHOPIFY_V2", "TESORERIA", "PAYOUTS", "RETIROS", "POSCOBRO_CAJA", "LEGACY_NO_TRAZABLE", "RUIDO_TECNICO", "PLACEHOLDERS"],
    },
    rules: {
      LEGAL_PRECEDENCE: "Si aparece o impacta DTE/factura/nota de crédito => incluir",
      TRACEABLE_NET_IMPACT: "Si tiene trazabilidad y afecta económicamente => incluir",
      FULL_NETTING: "Si netea completamente a cero => excluir",
      NO_TRACE_NO_LEGAL: "Sin trazabilidad y sin respaldo legal => excluir",
      TREASURY_OUT_OF_SCOPE: "Tesorería/caja fuera del modelo principal",
    },
    classifications: ["INGRESO", "COSTO_COMERCIAL", "COSTO_LOGISTICO", "DEVOLUCION", "AJUSTE_OPERATIVO", "RIESGO_FINANCIERO", "INDEFINIDO"],
    dictionary: [
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "VENTA_MARKETPLACE",
        clasificacion: "INGRESO",
        aliases: ["Cargo por venta", "Venta"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "COMISION_MARKETPLACE",
        clasificacion: "COSTO_COMERCIAL",
        aliases: ["Cargo por venta (Comisión)", "Anulación del cargo por venta", "Reembolso por comisión"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "LOGISTICA_MARKETPLACE",
        clasificacion: "COSTO_LOGISTICO",
        aliases: [
          "Cargo por envíos de Mercado Libre",
          "Cargo por Mercado Envíos",
          "Anulación del cargo por envíos de ML",
          "Anulación del cargo por Mercado Envíos",
          "Cargo por devolución",
          "Anulación del cargo por devolución",
          "Cargo por servicio de almacenamiento Full",
          "Cargo por retiro de stock Full",
          "Cargo por stock antiguo en Full",
          "Cargo por sobrepasar espacio Full",
          "Cargo por servicio de colecta Full",
          "Cargo por diferencias medidas/peso",
        ],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "PUBLICIDAD_MARKETPLACE",
        clasificacion: "COSTO_COMERCIAL",
        aliases: [
          "Cargo por campaña de publicidad - Product Ads",
          "Campañas de publicidad - Product Ads",
          "Cargo por campaña de publicidad - Brand Ads",
          "Campañas de publicidad - Brand Ads",
          "Campañas de publicidad - Display",
          "Cargo por campaña de publicidad - Display programático",
          "Anulación cargo publicidad Product Ads",
        ],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "SERVICIOS_COMERCIALES",
        clasificacion: "COSTO_COMERCIAL",
        aliases: ["Cargo por Asesoría Comercial", "Cargo por mantenimiento de Mi página", "Anulación mantenimiento Mi página"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "MERCADO_LIBRE",
        tipo_transaccion: "INGRESO_COMERCIAL",
        clasificacion: "INGRESO",
        aliases: ["Bonificación", "Rebate", "Compensación comercial"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "VENTA_MARKETPLACE",
        clasificacion: "INGRESO",
        aliases: ["Importe del pedido"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "COMISION_MARKETPLACE",
        clasificacion: "COSTO_COMERCIAL",
        aliases: ["Comisiones sobre pedidos", "Comisiones sobre pedidos reembolsados"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "LOGISTICA_MARKETPLACE",
        clasificacion: "COSTO_LOGISTICO",
        aliases: [
          "Gastos de envío pagados por el operador",
          "Gastos de envío reembolsados pagados por el operador",
          "Descuento por costo logístico",
          "Descuento por logística inversa",
        ],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "INGRESO_COMERCIAL",
        clasificacion: "INGRESO",
        aliases: ["Envío", "Despacho"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "DEVOLUCION_VENTA",
        clasificacion: "DEVOLUCION",
        aliases: ["Pedidos reembolsados"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "RIPLEY",
        tipo_transaccion: "AJUSTE_OPERATIVO",
        clasificacion: "AJUSTE_OPERATIVO",
        aliases: ["Descuento por cancelación", "Otros descuentos"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "PARIS",
        tipo_transaccion: "VENTA_MARKETPLACE",
        clasificacion: "INGRESO",
        aliases: ["Venta"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "PARIS",
        tipo_transaccion: "DEVOLUCION_VENTA",
        clasificacion: "DEVOLUCION",
        aliases: ["Devolución"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "PARIS",
        tipo_transaccion: "LOGISTICA_MARKETPLACE",
        clasificacion: "COSTO_LOGISTICO",
        aliases: [
          "Cobro por despacho",
          "Logística inversa",
          "Retiro stock bodega Paris",
          "Cobro stock antiguo",
          "Multa",
          "Multa por stock",
        ],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "PARIS",
        tipo_transaccion: "INGRESO_COMERCIAL",
        clasificacion: "INGRESO",
        aliases: ["Despacho", "Rebate"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "PARIS",
        tipo_transaccion: "AJUSTE_OPERATIVO",
        clasificacion: "AJUSTE_OPERATIVO",
        aliases: ["Compensación logística", "Ajuste Inventario Activo", "Cobro por campaña", "Merma"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "FALABELLA",
        tipo_transaccion: "VENTA_MARKETPLACE",
        clasificacion: "INGRESO",
        aliases: ["Sale amount", "Gross sales", "Pago por precio del producto"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "FALABELLA",
        tipo_transaccion: "COMISION_MARKETPLACE",
        clasificacion: "COSTO_COMERCIAL",
        aliases: ["Cobro por comisión por venta", "Reembolso por comisión por venta"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "FALABELLA",
        tipo_transaccion: "LOGISTICA_MARKETPLACE",
        clasificacion: "COSTO_LOGISTICO",
        aliases: [
          "Cobro por cofinanciamiento logístico",
          "Reversa de pago de envío comprador",
          "Cobro por logística inversa",
          "Pago por envío directo",
        ],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
      {
        marketplace: "FALABELLA",
        tipo_transaccion: "AJUSTE_OPERATIVO",
        clasificacion: "AJUSTE_OPERATIVO",
        aliases: ["Corrección de pago envio directo", "Corrección de cobro por envío directo"],
        respaldo_legal: true,
        trazabilidad: "FULL",
        decision: "INCLUIR",
      },
    ],
  };

  // 2. Guardar el dictionary como JSON
  const jsonPath = path.join(ROOT, "master_marketplace_dictionary_v1.json");
  await writeFile(jsonPath, JSON.stringify(dict, null, 2), "utf-8");
  console.log(`✓ Dictionary saved to ${jsonPath}`);

  // 3. Generar el RAW_TO_CLASSIFICATION_MAP a partir del dictionary
  const rawMap = {};
  const canonicalToClasif = {};

  for (const entry of dict.dictionary) {
    const mp = entry.marketplace;
    for (const alias of entry.aliases) {
      // Mapeo raw → canonical (tipo_transaccion calificado con marketplace)
      const rawKey = alias;
      const canonicalValue = `${alias}`;
      rawMap[rawKey] = canonicalValue;
    }
    // Mapeo canonical → clasificación
    for (const alias of entry.aliases) {
      canonicalToClasif[alias] = entry.clasificacion;
    }
  }

  // 4. Generar FINANCIAL_STRUCTURE
  const structure = {
    ingresos: [],
    devoluciones: [],
    costos_operacionales: [],
    costos_comerciales: [],
    ajustes: [],
    tesoreria: ["Retiro de dinero"],
  };

  for (const entry of dict.dictionary) {
    const clasif = entry.clasificacion;
    for (const alias of entry.aliases) {
      switch (clasif) {
        case "INGRESO":
          structure.ingresos.push(alias);
          break;
        case "DEVOLUCION":
          structure.devoluciones.push(alias);
          break;
        case "COSTO_LOGISTICO":
          structure.costos_operacionales.push(alias);
          break;
        case "COSTO_COMERCIAL":
          structure.costos_comerciales.push(alias);
          break;
        case "AJUSTE_OPERATIVO":
          structure.ajustes.push(alias);
          break;
      }
    }
  }

  // 5. Read current marketplace_auditor.py and rebuild it
  const auditorPath = path.join(ROOT, "engine", "v4", "marketplace_auditor.py");
  const current = await readFile(auditorPath, "utf-8");

  // Find the boundaries of RAW_TO_CLASSIFICATION_MAP
  const rawMapStart = current.indexOf("RAW_TO_CLASSIFICATION_MAP = {");
  const rawMapEnd = current.indexOf("}", rawMapStart) + 1;
  const afterRawMap = current.slice(rawMapEnd);

  // Find FINANCIAL_STRUCTURE boundaries
  const finStart = current.indexOf("FINANCIAL_STRUCTURE = {");
  const finEnd = current.indexOf("}", finStart) + 1;
  const afterFin = current.slice(finEnd);

  // 6. Build new RAW_TO_CLASSIFICATION_MAP string
  //    (preserving existing entries not in dictionary, like encoding variants)
  const existingLines = current.slice(rawMapStart, rawMapEnd).split("\n");
  const existingEntries = {};
  for (const line of existingLines) {
    const m = line.match(/^\s*"(.+?)":\s*"(.+?)",?\s*$/);
    if (m) existingEntries[m[1]] = m[2];
  }

  // Merge: dictionary entries take precedence
  for (const [k, v] of Object.entries(rawMap)) {
    existingEntries[k] = v;
  }

  // Format as Python
  const newRawMapLines = Object.entries(existingEntries).map(
    ([k, v]) => `    "${k}": "${v}",`
  );
  const newRawMapBlock = `RAW_TO_CLASSIFICATION_MAP = {\n${newRawMapLines.join("\n")}\n}`;

  // 7. Build new FINANCIAL_STRUCTURE
  const newFinLines = [];
  for (const [group, items] of Object.entries(structure)) {
    const quoted = items.map((i) => `"${i}"`).join(",\n        ");
    newFinLines.push(`    "${group}": [\n        ${quoted}\n    ]`);
  }
  const newFinBlock = `FINANCIAL_STRUCTURE = {\n${newFinLines.join(",\n")}\n}`;

  // 8. Write updated file
  const newContent =
    current.slice(0, rawMapStart) +
    newRawMapBlock +
    "\n\n" +
    current.slice(rawMapEnd + 1, finStart) +
    newFinBlock +
    afterFin;

  await writeFile(auditorPath, newContent, "utf-8");
  console.log(`✓ Updated ${auditorPath}`);
  console.log(`  RAW_TO_CLASSIFICATION_MAP: ${Object.keys(existingEntries).length} entries`);
  console.log(`  FINANCIAL_STRUCTURE groups: ${Object.keys(structure).length}`);
}

main().catch(console.error);
