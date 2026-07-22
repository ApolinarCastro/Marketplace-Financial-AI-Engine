import re

def patch_dashboard():
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update detailsMap to dynamically accept any category
    old_details_map = """            const detailsMap = {
                ingresos: {}, devoluciones: {}, costos_operacionales: {}, costos_comerciales: {}, ajustes: {}
            };"""
    
    new_details_map = """            const detailsMap = {
                ingresos: {}, devoluciones: {}, costos_operacionales: {}, costos_comerciales: {}, ajustes: {}, sin_clasificar: {}, UNKNOWN: {}
            };"""
    
    if old_details_map in content:
        content = content.replace(old_details_map, new_details_map)

    old_if_cat = """                if (cat && detailsMap[cat]) {"""
    new_if_cat = """                if (cat) {
                    if (!detailsMap[cat]) detailsMap[cat] = {};"""
    
    if old_if_cat in content:
        content = content.replace(old_if_cat, new_if_cat)

    # 2. Add IDs to sections so we can hide them
    content = content.replace('<!-- CAPA OPERACIONAL Y TRANSACCIONAL -->\n        <section class="mt-8">', '<!-- CAPA OPERACIONAL Y TRANSACCIONAL -->\n        <section class="mt-8 hidden" id="sect-operacional">')
    content = content.replace('<!-- CAPA LIQUIDACIÓN -->\n        <section class="mt-8">', '<!-- CAPA LIQUIDACIÓN -->\n        <section class="mt-8 hidden" id="sect-liquidacion">')
    # handle possible encoding issue with LIQUIDACIN
    content = re.sub(r'<!-- CAPA LIQUIDACI.N -->\s*<section class="mt-8">', '<!-- CAPA LIQUIDACION -->\n        <section class="mt-8 hidden" id="sect-liquidacion">', content)
    
    content = re.sub(r'<!-- CAPA TESORER.A -->\s*<section class="mt-8">', '<!-- CAPA TESORERIA -->\n        <section class="mt-8 hidden" id="sect-tesoreria">', content)
    
    content = re.sub(r'<h2 class="text-lg font-bold text-slate-800 mb-4 mt-8">Cobertura Documental \(DTE\)</h2>\s*<p id="dte-explanation" class="text-xs text-slate-500 mb-4 hidden">', '<section class="mt-8 hidden" id="sect-cobertura">\n        <h2 class="text-lg font-bold text-slate-800 mb-4">Cobertura Documental (DTE)</h2>\n        <p id="dte-explanation" class="text-xs text-slate-500 mb-4 hidden">', content)
    content = content.replace('<div class="card p-5 bg-slate-800 text-white shadow-lg"><span class="kpi-label text-slate-300">Cobertura</span><div class="kpi-value-primary mt-1" id="ux12-doc-cov">—</div></div>\n        </div>', '<div class="card p-5 bg-slate-800 text-white shadow-lg"><span class="kpi-label text-slate-300">Cobertura</span><div class="kpi-value-primary mt-1" id="ux12-doc-cov">—</div></div>\n        </div>\n        </section>')

    # 3. Update loadAnalyticLayers to hide/show sections based on data
    js_update = """
            if (v3Data) {
                // Operacional
                const isOpZero = v3Data.operacional.venta_mp === 0 && v3Data.operacional.costos_logisticos === 0 && v3Data.operacional.movimiento_financiero === 0;
                if (!isOpZero) {
                    document.getElementById('sect-operacional').classList.remove('hidden');
                } else {
                    document.getElementById('sect-operacional').classList.add('hidden');
                }
                
                document.getElementById('v3-op-venta-mp').textContent = fmtCLP(v3Data.operacional.venta_mp);
                document.getElementById('v3-op-venta-ff').textContent = fmtCLP(v3Data.operacional.costos_logisticos);
                document.getElementById('v3-op-venta-cons').textContent = fmtCLP(v3Data.operacional.movimiento_financiero);
                document.getElementById('v3-op-ord-mp').textContent = fmtNumber(v3Data.operacional.ordenes_mp);
                document.getElementById('v3-op-ord-ff').textContent = fmtNumber(v3Data.operacional.ordenes_ff);

                // Liquidación
                const isLiqZero = v3Data.liquidacion.venta_liquidada === 0 && v3Data.liquidacion.comision_liquidada === 0 && v3Data.liquidacion.ajustes_liquidacion === 0 && v3Data.liquidacion.liquidacion_neta === 0;
                if (!isLiqZero) {
                    document.getElementById('sect-liquidacion').classList.remove('hidden');
                } else {
                    document.getElementById('sect-liquidacion').classList.add('hidden');
                }

                document.getElementById('v3-liq-venta').textContent = fmtCLP(v3Data.liquidacion.venta_liquidada);
                document.getElementById('v3-liq-com').textContent = fmtCLP(v3Data.liquidacion.comision_liquidada);
                document.getElementById('v3-liq-aj').textContent = fmtCLP(v3Data.liquidacion.ajustes_liquidacion);
                document.getElementById('v3-liq-neto').textContent = fmtCLP(v3Data.liquidacion.liquidacion_neta);

                // Tesorería
                const isTesZero = v3Data.tesoreria.disponible === 0 && v3Data.tesoreria.transferencias === 0 && v3Data.tesoreria.pagos_recibidos === 0;
                if (!isTesZero) {
                    document.getElementById('sect-tesoreria').classList.remove('hidden');
                } else {
                    document.getElementById('sect-tesoreria').classList.add('hidden');
                }

                document.getElementById('v3-tes-disp').textContent = fmtCLP(v3Data.tesoreria.disponible);
                document.getElementById('v3-tes-trans').textContent = fmtCLP(v3Data.tesoreria.transferencias);
                document.getElementById('v3-tes-pagos').textContent = fmtCLP(v3Data.tesoreria.pagos_recibidos);
            }
"""

    old_js = """
            if (v3Data) {
                // Operacional
                document.getElementById('v3-op-venta-mp').textContent = fmtCLP(v3Data.operacional.venta_mp);
                document.getElementById('v3-op-venta-ff').textContent = fmtCLP(v3Data.operacional.costos_logisticos);
                document.getElementById('v3-op-venta-cons').textContent = fmtCLP(v3Data.operacional.movimiento_financiero);
                document.getElementById('v3-op-ord-mp').textContent = fmtNumber(v3Data.operacional.ordenes_mp);
                document.getElementById('v3-op-ord-ff').textContent = fmtNumber(v3Data.operacional.ordenes_ff);

                // Liquidacin
                document.getElementById('v3-liq-venta').textContent = fmtCLP(v3Data.liquidacion.venta_liquidada);
                document.getElementById('v3-liq-com').textContent = fmtCLP(v3Data.liquidacion.comision_liquidada);
                document.getElementById('v3-liq-aj').textContent = fmtCLP(v3Data.liquidacion.ajustes_liquidacion);
                document.getElementById('v3-liq-neto').textContent = fmtCLP(v3Data.liquidacion.liquidacion_neta);

                // Tesorera
                document.getElementById('v3-tes-disp').textContent = fmtCLP(v3Data.tesoreria.disponible);
                document.getElementById('v3-tes-trans').textContent = fmtCLP(v3Data.tesoreria.transferencias);
                document.getElementById('v3-tes-pagos').textContent = fmtCLP(v3Data.tesoreria.pagos_recibidos);
            }
"""
    # handle possible encoding issue with LIQUIDACIN
    content = re.sub(r'if \(v3Data\) \{\s*// Operacional.*?// Tesorer.*?pagos_recibidos\);\s*\}', js_update.strip(), content, flags=re.DOTALL)

    # 4. Documentary section
    doc_update = """
            // Populate Documentary section
            let docStats = summary.total_documentary || { xml_conciliados: 0, xml_pendientes: 0, total_dte: 0, cobertura: 0 };
            if (mp && mp !== 'ALL') {
                const target = summary.marketplaces.find(m => m.id === mp);
                if (target && target.documentary) {
                    docStats = target.documentary;
                }
            }
            const isDocZero = docStats.total_dte === 0;
            if (!isDocZero) {
                document.getElementById('sect-cobertura').classList.remove('hidden');
            } else {
                document.getElementById('sect-cobertura').classList.add('hidden');
            }
            document.getElementById('ux12-doc-match').textContent = fmtNumber(docStats.xml_conciliados);
"""
    content = re.sub(r'// Populate Documentary section.*?(?=document\.getElementById\(\'ux12-doc-match\'\))', doc_update.strip() + '\n            ', content, flags=re.DOTALL)


    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

patch_dashboard()
