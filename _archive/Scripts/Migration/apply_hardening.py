import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML Placeholders
content = content.replace('Factura Electr\u00f3nica (33)', '<span id=\'cert-doc-type-text\'>-</span>')
content = content.replace('Factura Electrónica (33)', '<span id=\'cert-doc-type-text\'>-</span>')
content = content.replace('<span class=\"text-white font-mono\">123456</span>', '<span class=\"text-white font-mono\" id=\"cert-doc-folio-text\">-</span>')
content = content.replace('Validar folios SII pendientes (Prioridad Alta)', '-')
content = content.replace('Recopilar evidencias de anulaci\u00f3n', '-')
content = content.replace('Recopilar evidencias de anulación', '-')

# 2. JS Logic Replacement
js_start_idx = content.find('// --- Certification Drawer Logic ---')
if js_start_idx != -1:
    js_end_idx = content.find('</script>', js_start_idx)
    new_js = '''// --- Certification Drawer Logic ---
    let currentCertPayload = null;
    
    async function openCertificationDrawer(txId, status) {
        document.getElementById('cert-drawer').classList.remove('translate-x-full');
        document.getElementById('cert-drawer-overlay').classList.remove('hidden');
        document.getElementById('cert-tx-id').innerText = txId || 'N/A';
        
        // Reset state
        ['pipe-xml', 'pipe-xsd', 'pipe-sig', 'pipe-caf'].forEach(id => {
            const el = document.getElementById(id);
            el.className = 'text-[10px] font-bold px-2 py-0.5 rounded bg-slate-700';
            el.innerText = 'PENDING';
        });
        document.getElementById('cert-status').innerText = '-';
        document.getElementById('cert-status').className = 'font-bold text-slate-400';
        document.getElementById('btn-obsidian').classList.add('hidden');
        document.getElementById('cert-doc-type-text').innerText = '-';
        document.getElementById('cert-doc-folio-text').innerText = '-';
        document.getElementById('ev-hash').innerText = '-';
        document.getElementById('ev-conf').innerText = '-';
        document.getElementById('cert-hash').innerText = '-';
        document.getElementById('cert-level').innerText = '-';
        
        if (status !== 'CONCILIADO' && status !== 'DOCUMENTADO') {
            document.getElementById('cert-upload-zone').classList.remove('hidden');
        } else {
            document.getElementById('cert-upload-zone').classList.add('hidden');
            try {
                const res = await ApiClient.safeFetch('/api/v4/electronic_certification/status/' + txId);
                // Handled normally it shouldn't get here unless it succeeds
                if (res.status === 'BLOCKED') {
                    renderBlockedDrawer('BACKEND CONTRACT REQUIRED');
                } else if (res.status === 'NOT_FOUND') {
                    renderBlockedDrawer('XML_NOT_AVAILABLE');
                } else {
                    currentCertPayload = res;
                    applyCertResultToDrawer(res);
                }
            } catch (err) {
                renderBlockedDrawer('BACKEND DATA NOT AVAILABLE\\nMissing Contract\\nImplementation Blocked');
            }
        }
    }

    function renderBlockedDrawer(message) {
        document.getElementById('cert-status').innerText = 'BLOCKED';
        document.getElementById('cert-status').className = 'font-bold text-rose-500';
        document.getElementById('cert-hash').innerText = message;
        document.getElementById('cert-hash').className = 'text-[10px] font-mono text-rose-400 font-bold uppercase whitespace-pre-line';
    }
    
    function closeCertificationDrawer() {
        document.getElementById('cert-drawer').classList.add('translate-x-full');
        document.getElementById('cert-drawer-overlay').classList.add('hidden');
    }
    
    async function processXMLUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        document.getElementById('cert-upload-zone').classList.add('hidden');
        
        const reader = new FileReader();
        reader.onload = async function(e) {
            const xmlContent = e.target.result;
            try {
                const mp = document.getElementById('marketplace-selector').value;
                const response = await fetch('/api/v4/electronic_certification/validate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/xml',
                        'X-Marketplace': mp
                    },
                    body: xmlContent
                });
                const res = await response.json();
                if (res.status === 'success') {
                    currentCertPayload = res.data;
                    applyCertResultToDrawer(currentCertPayload);
                } else {
                    renderBlockedDrawer(res.message || 'Validation Failed');
                }
            } catch (err) {
                renderBlockedDrawer('BACKEND ERROR: ' + err.message);
            }
        };
        reader.readAsText(file);
    }
    
    function applyCertResultToDrawer(payload) {
        if (!payload || !payload.certification_result) return;
        
        const isPass = payload.certification_result.certification_status === 'PASS' || payload.certification_result.certification_status === 'CERTIFIED' || payload.certification_result.certification_status === 'RECONCILED';
        
        const passClass = 'text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-900 text-emerald-400';
        const failClass = 'text-[10px] font-bold px-2 py-0.5 rounded bg-rose-900 text-rose-400';
        const warnClass = 'text-[10px] font-bold px-2 py-0.5 rounded bg-amber-900 text-amber-400';
        
        // E06 - Pipeline exact states
        const stages = payload.certification_result.stages || [];
        const pipeMap = {'XML': 'pipe-xml', 'XSD': 'pipe-xsd', 'Signature': 'pipe-sig', 'CAF': 'pipe-caf'};
        
        stages.forEach(st => {
            const id = pipeMap[st.stage];
            if (id) {
                const el = document.getElementById(id);
                el.innerText = st.status;
                if (st.status === 'PASS') el.className = passClass;
                else if (st.status === 'WARNING') el.className = warnClass;
                else el.className = failClass;
            }
        });
        
        const statusEl = document.getElementById('cert-status');
        statusEl.innerText = payload.certification_result.certification_status || 'UNKNOWN';
        statusEl.className = isPass ? 'font-bold text-emerald-400' : 'font-bold text-rose-400';
        
        // Metadata if available
        if (payload.dte_metadata) {
            document.getElementById('cert-doc-type-text').innerText = payload.dte_metadata.tipo_dte || '-';
            document.getElementById('cert-doc-folio-text').innerText = payload.dte_metadata.folio || '-';
        }

        // Evidence E07
        document.getElementById('cert-level').innerText = payload.evidence ? payload.evidence.confidence > 0 ? 'CRYPTOGRAPHIC' : 'NONE' : 'NONE';
        const h = payload.evidence ? payload.evidence.hash : 'NO_EVIDENCE';
        document.getElementById('cert-hash').innerText = h;
        document.getElementById('cert-hash').className = 'text-xs font-mono truncate';
        document.getElementById('ev-hash').innerText = h;
        document.getElementById('ev-conf').innerText = payload.evidence ? payload.evidence.confidence : '0.0';
        
        // Obsidian E08
        if (isPass) {
            document.getElementById('btn-obsidian').classList.remove('hidden');
        }
    }
    
    async function exportToObsidian() {
        if (!currentCertPayload) {
            alert('No payload to export');
            return;
        }
        try {
            const res = await fetch('/api/v4/knowledge/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentCertPayload)
            });
            const data = await res.json();
            if (data.status === 'success') {
                alert('Exportado a Obsidian correctamente');
            } else {
                alert('Error al exportar: ' + data.message);
            }
        } catch (e) {
            console.error(e);
            alert('Error al exportar: ' + e);
        }
    }
'''
    content = content[:js_start_idx] + new_js + '\n' + content[js_end_idx:]

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated templates/dashboard.html successfully")
