import re

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

drawer_code = """
        // Exposed to global scope
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
                        
                        const setPipe = (id, status) => {
                            const el = document.getElementById(id);
                            if(el) {
                                el.innerText = status || '-';
                                el.className = (status === 'PASS') 
                                    ? 'text-[10px] font-bold px-2 py-0.5 rounded bg-green-900 text-green-300' 
                                    : 'text-[10px] font-bold px-2 py-0.5 rounded bg-slate-700 text-slate-300';
                            }
                        };
                        setPipe('pipe-xml', pipe.xml?.status);
                        setPipe('pipe-xsd', pipe.xsd?.status);
                        setPipe('pipe-sig', pipe.signature?.status);
                        setPipe('pipe-caf', pipe.caf?.status);
                        
                        const ev = res.evidence || {};
                        const docCertStatus = res.document_certification ? res.document_certification.status : '-';
                        
                        const certStatusEl = document.getElementById('cert-status');
                        certStatusEl.innerText = docCertStatus;
                        
                        if (docCertStatus === 'PASS') {
                            certStatusEl.className = 'font-bold text-emerald-400';
                        } else if (docCertStatus === 'BLOCKED_BY_SOURCE_DATA' || docCertStatus === 'NOT_FOUND') {
                            certStatusEl.className = 'font-bold text-amber-500';
                        } else {
                            certStatusEl.className = 'font-bold text-rose-500';
                        }
                        
                        document.getElementById('cert-level').innerText = ev.evidence_level || 'DESCONOCIDO';
                        document.getElementById('cert-hash').innerText = ev.evidence_hash ? ev.evidence_hash.substring(0,20) : '-';
                        document.getElementById('ev-hash').innerText = ev.evidence_hash || '-';
                        document.getElementById('ev-conf').innerText = ev.confidence_score ? ev.confidence_score + '%' : 'N/A';
                    } else {
                        document.getElementById('cert-status').innerText = res?.status || 'NOT_FOUND';
                        document.getElementById('cert-status').className = 'font-bold text-slate-400';
                        document.getElementById('cert-level').innerText = 'DESCONOCIDO';
                        document.getElementById('cert-hash').innerText = '-';
                        document.getElementById('ev-hash').innerText = '-';
                        document.getElementById('ev-conf').innerText = 'N/A';
                    }
                } catch(e) {
                    console.error("Error loading drawer details", e);
                    document.getElementById('cert-status').innerText = 'ERROR';
                    document.getElementById('cert-status').className = 'font-bold text-red-500';
                }

                if (typeof loadDocumentaryInsights === 'function') {
                    loadDocumentaryInsights();
                }
            },
            closeCertificationDrawer() {
                const drawer = document.getElementById('cert-drawer');
                const overlay = document.getElementById('cert-drawer-overlay');
                if (drawer) drawer.classList.replace('translate-x-0', 'translate-x-full');
                if (overlay) overlay.classList.add('hidden');
            }
        };
"""
if "DocumentModule = {" not in content:
    content = content.replace("</script>", drawer_code + "\n</script>", 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved dashboard.html with drawer code")
