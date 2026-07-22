import re

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = r"""        // Exposed to global scope
        function openCertificationDrawer(tx_id, estado) {
            DocumentModule.openCertificationDrawer(tx_id, estado);
        }
        function closeCertificationDrawer() {
            DocumentModule.closeCertificationDrawer();
        }
        
        const DocumentModule = {
            currentTxId: null,

            async openCertificationDrawer(transaction_id, estado_xml) {
                this.currentTxId = transaction_id;
                
                const drawer = document.getElementById('cert-drawer');
                const overlay = document.getElementById('cert-drawer-overlay');
                if (drawer) drawer.classList.replace('translate-x-full', 'translate-x-0');
                if (overlay) overlay.classList.remove('hidden');
                
                const container = document.getElementById('ai-insights-container');
                if (container) container.classList.remove('hidden');

                try {
                    document.getElementById('cert-status').innerText = 'Cargando...';
                    document.getElementById('cert-status').className = 'font-bold text-slate-300';
                    document.getElementById('cert-tx-id').innerText = transaction_id;
                    
                    const res = await ApiClient.safeFetch(/api/v4/electronic_certification/status/);
                    if (res && res.document_certification) {
                        const dt = res.document_trace || {};
                        document.getElementById('cert-doc-type-text').innerText = dt.tipo_dte || '-';
                        document.getElementById('cert-doc-folio-text').innerText = dt.folio || '-';
                        
                        const elEmisor = document.getElementById('cert-doc-emisor');
                        if(elEmisor) elEmisor.innerText = dt.emisor || '-';
                        const elReceptor = document.getElementById('cert-doc-receptor');
                        if(elReceptor) elReceptor.innerText = dt.receptor || '-';
                        const elFecha = document.getElementById('cert-doc-fecha');
                        if(elFecha) elFecha.innerText = dt.fecha_emision || '-';
                        const elMonto = document.getElementById('cert-doc-monto');
                        if(elMonto) elMonto.innerText = dt.monto_total ? $ + dt.monto_total.toLocaleString('es-CL') : 'No Declarado';

                        const pipe = res.pipeline || {};
                        const risk = res.risk_analysis || {};
                        
                        let estadoTexto = "Desconocido";
                        let colorEstado = "text-slate-500";
                        if (pipe.status === "VALIDATED") {
                            estadoTexto = "Validado";
                            colorEstado = "text-emerald-500";
                        } else if (pipe.status === "BLOCKED_BY_SOURCE_DATA") {
                            estadoTexto = "Bloqueado (Sin Origen)";
                            colorEstado = "text-amber-500";
                        } else if (pipe.status === "MISSING_SETTLEMENT") {
                            estadoTexto = "Sin Liquidación";
                            colorEstado = "text-amber-500";
                        }
                        document.getElementById('cert-status').innerText = estadoTexto;
                        document.getElementById('cert-status').className = `font-bold ${colorEstado}`;
                        
                        document.getElementById('tax-risk-metrics').innerHTML = `<p class='text-xs text-slate-600'>Análisis: ${risk.level || 'Sin datos'}</p>`;
                        document.getElementById('doc-recommendations').innerHTML = `<p class='text-xs text-slate-600'>${(risk.factors || []).join(', ') || 'Ninguna'}</p>`;
                    } else {
                        throw new Error("No data");
                    }
                } catch(e) {
                    console.error("Drawer error:", e);
                    document.getElementById('cert-status').innerText = estado_xml || 'PENDIENTE';
                }
            },
            closeCertificationDrawer() {
                const drawer = document.getElementById('cert-drawer');
                const overlay = document.getElementById('cert-drawer-overlay');
                if (drawer) drawer.classList.replace('translate-x-0', 'translate-x-full');
                if (overlay) overlay.classList.add('hidden');
                
                const container = document.getElementById('ai-insights-container');
                if (container) container.classList.add('hidden');
                this.currentTxId = null;
            }
        };"""

replacement = """        // Exposed to global scope
        function openCertificationDrawer(tx_id, estado) {
            DocumentModule.openCertificationDrawer(tx_id, estado);
        }
        function closeCertificationDrawer() {
            DocumentModule.closeCertificationDrawer();
        }
        
        const DocumentModule = {
            currentTxId: null,

            async openCertificationDrawer(transaction_id, estado_xml) {
                this.currentTxId = transaction_id;
                
                const drawer = document.getElementById('cert-drawer');
                const overlay = document.getElementById('cert-drawer-overlay');
                if (drawer) drawer.classList.replace('translate-x-full', 'translate-x-0');
                if (overlay) overlay.classList.remove('hidden');
                
                const container = document.getElementById('ai-insights-container');
                if (container) container.classList.remove('hidden');

                try {
                    document.getElementById('cert-status').innerText = 'Cargando...';
                    document.getElementById('cert-status').className = 'font-bold text-slate-300';
                    document.getElementById('cert-tx-id').innerText = transaction_id;
                    
                    const res = await ApiClient.safeFetch(`/api/v4/electronic_certification/status/${transaction_id}`);
                    if (res && res.document_certification) {
                        const dt = res.document_trace || {};
                        document.getElementById('cert-doc-type-text').innerText = dt.tipo_dte || '-';
                        document.getElementById('cert-doc-folio-text').innerText = dt.folio || '-';
                        
                        const elEmisor = document.getElementById('cert-doc-emisor');
                        if(elEmisor) elEmisor.innerText = dt.emisor || '-';
                        const elReceptor = document.getElementById('cert-doc-receptor');
                        if(elReceptor) elReceptor.innerText = dt.receptor || '-';
                        const elFecha = document.getElementById('cert-doc-fecha');
                        if(elFecha) elFecha.innerText = dt.fecha_emision || '-';
                        const elMonto = document.getElementById('cert-doc-monto');
                        if(elMonto) elMonto.innerText = dt.monto_total ? `$${dt.monto_total.toLocaleString('es-CL')}` : 'No Declarado';

                        const pipe = res.pipeline || {};
                        const risk = res.risk_analysis || {};
                        
                        let estadoTexto = "Desconocido";
                        let colorEstado = "text-slate-500";
                        if (pipe.status === "VALIDATED") {
                            estadoTexto = "Validado";
                            colorEstado = "text-emerald-500";
                        } else if (pipe.status === "BLOCKED_BY_SOURCE_DATA") {
                            estadoTexto = "Bloqueado (Sin Origen)";
                            colorEstado = "text-amber-500";
                        } else if (pipe.status === "MISSING_SETTLEMENT") {
                            estadoTexto = "Sin Liquidación";
                            colorEstado = "text-amber-500";
                        }
                        document.getElementById('cert-status').innerText = estadoTexto;
                        document.getElementById('cert-status').className = `font-bold ${colorEstado}`;
                        
                        document.getElementById('tax-risk-metrics').innerHTML = `<p class='text-xs text-slate-600'>Análisis: ${risk.level || 'Sin datos'}</p>`;
                        document.getElementById('doc-recommendations').innerHTML = `<p class='text-xs text-slate-600'>${(risk.factors || []).join(', ') || 'Ninguna'}</p>`;
                    } else {
                        throw new Error("No data");
                    }
                } catch(e) {
                    console.error("Drawer error:", e);
                    document.getElementById('cert-status').innerText = estado_xml || 'PENDIENTE';
                }
            },
            closeCertificationDrawer() {
                const drawer = document.getElementById('cert-drawer');
                const overlay = document.getElementById('cert-drawer-overlay');
                if (drawer) drawer.classList.replace('translate-x-0', 'translate-x-full');
                if (overlay) overlay.classList.add('hidden');
                
                const container = document.getElementById('ai-insights-container');
                if (container) container.classList.add('hidden');
                this.currentTxId = null;
            }
        };"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Drawer replaced")
else:
    print("Not found drawer target")
