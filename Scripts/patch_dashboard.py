import re

def patch_dashboard():
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        dash_content = f.read()

    with open('templates/executive_dashboard.html', 'r', encoding='utf-8') as f:
        exec_content = f.read()

    # Extract HTML components
    start_idx = exec_content.find('<!-- CAPA OPERACIONAL Y TRANSACCIONAL -->')
    end_idx = exec_content.find('</main>')
    html_components = exec_content[start_idx:end_idx]

    # Extract JS
    js_start = exec_content.find('// ── Main Load V3 ──')
    js_end = exec_content.find('// Scorecard')
    js_v3 = exec_content[js_start:js_end]

    js_wf_start = exec_content.find('async function loadWaterfallV3')
    js_wf_end = exec_content.find('// Initial load')
    js_wf = exec_content[js_wf_start:js_wf_end]

    # Insert HTML into dashboard.html just before </main>
    if '<!-- CAPA OPERACIONAL Y TRANSACCIONAL -->' not in dash_content:
        dash_content = dash_content.replace('</main>', '\n        <div class="col-span-12 mt-8">\n' + html_components + '\n        </div>\n</main>')

    # Insert JS functions
    if 'async function loadWaterfallV3' not in dash_content:
        dash_content = dash_content.replace('</script>\n</body>', '\n' + js_wf + '\n</script>\n</body>')

    # We need to call the loading logic inside loadDashboard
    # Let's see where to inject the load v3 call
    # We will just write a wrapper loadAnalyticLayers() and call it inside loadDashboard
    
    analytic_loader = """
    async function loadAnalyticLayers() {
        const period = document.getElementById('period').value;
        const mp = document.getElementById('mp').value;
        
        const summaryUrl = '/api/v4/exec/summary' + (period !== 'ALL' && period !== 'YTD' ? '?periodo=' + period : '');
        
        const v3Params = new URLSearchParams();
        if (period !== 'ALL' && period !== 'YTD') v3Params.set('periodo', period);
        if (mp && mp !== 'ALL') v3Params.set('marketplace', mp);
        const v3Url = '/api/v4/exec/summary-v3?' + v3Params.toString();

        try {
            const [summaryRes, v3Res] = await Promise.all([fetch(summaryUrl), fetch(v3Url)]);
            
            let summary = { marketplaces: [] };
            if (summaryRes.ok) summary = await summaryRes.json();
            
            let v3Data = null;
            if (v3Res.ok) v3Data = await v3Res.json();

            if (v3Data) {
                // Operacional
                document.getElementById('v3-op-venta-mp').textContent = fmtCLP(v3Data.operacional.venta_mp);
                document.getElementById('v3-op-venta-ff').textContent = fmtCLP(v3Data.operacional.costos_logisticos);
                document.getElementById('v3-op-venta-cons').textContent = fmtCLP(v3Data.operacional.movimiento_financiero);
                document.getElementById('v3-op-ord-mp').textContent = fmtNumber(v3Data.operacional.ordenes_mp);
                document.getElementById('v3-op-ord-ff').textContent = fmtNumber(v3Data.operacional.ordenes_ff);

                // Liquidación
                document.getElementById('v3-liq-venta').textContent = fmtCLP(v3Data.liquidacion.venta_liquidada);
                document.getElementById('v3-liq-com').textContent = fmtCLP(v3Data.liquidacion.comision_liquidada);
                document.getElementById('v3-liq-aj').textContent = fmtCLP(v3Data.liquidacion.ajustes_liquidacion);
                document.getElementById('v3-liq-neto').textContent = fmtCLP(v3Data.liquidacion.liquidacion_neta);

                // Tesorería
                document.getElementById('v3-tes-disp').textContent = fmtCLP(v3Data.tesoreria.disponible);
                document.getElementById('v3-tes-trans').textContent = fmtCLP(v3Data.tesoreria.transferencias);
                document.getElementById('v3-tes-pagos').textContent = fmtCLP(v3Data.tesoreria.pagos_recibidos);
            }

            // Populate Documentary section
            let docStats = summary.total_documentary || { xml_conciliados: 0, xml_pendientes: 0, total_dte: 0, cobertura: 0 };
            if (mp && mp !== 'ALL') {
                const target = summary.marketplaces.find(m => m.id === mp);
                if (target && target.documentary) {
                    docStats = target.documentary;
                }
            }
            document.getElementById('ux12-doc-match').textContent = fmtNumber(docStats.xml_conciliados);
            document.getElementById('ux12-doc-pend').textContent = fmtNumber(docStats.xml_pendientes);
            document.getElementById('ux12-doc-total').textContent = fmtNumber(docStats.total_dte);
            document.getElementById('ux12-doc-cov').textContent = docStats.cobertura.toFixed(1) + '%';
        } catch (e) {
            console.error("Error loading analytic layers", e);
        }

        // Load Waterfalls
        loadWaterfallV3('operacional');
        loadWaterfallV3('liquidacion');
    }
"""
    if 'loadAnalyticLayers' not in dash_content:
        dash_content = dash_content.replace('</script>\n</body>', '\n' + analytic_loader + '\n</script>\n</body>')
        
    # Inject call into loadDashboard
    if 'loadAnalyticLayers();' not in dash_content:
        dash_content = dash_content.replace('renderCierre();', 'renderCierre();\n            loadAnalyticLayers();')

    # Also add fmtCLP and fmtNumber if they don't exist
    if 'const fmtCLP' not in dash_content:
        dash_content = dash_content.replace('function loadDashboard() {', "const fmtCLP = v => new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(v);\n        const fmtNumber = v => new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 }).format(v);\n\n        function loadDashboard() {")

    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dash_content)
        
    print("Dashboard patched successfully.")

patch_dashboard()
