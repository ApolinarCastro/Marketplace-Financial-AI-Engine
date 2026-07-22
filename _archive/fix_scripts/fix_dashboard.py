import re
import traceback

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the status hardcode
old_status = """if (DashboardState._hasAuditAlerts) {
                    estadoContainer.innerHTML = `
                        <div class="surgical-card p-4 shadow-sm bg-amber-50 border-amber-200">
                            <h3 class="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-1"><i class="fas fa-exclamation-triangle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-amber-800 font-bold">En Revisión</p>
                        </div>`;
                } else if (DashboardState._financialStructure && DashboardState._financialStructure.categories && DashboardState._financialStructure.categories.length > 0) {
                    estadoContainer.innerHTML = `
                        <div class="surgical-card p-4 shadow-sm bg-emerald-50 border-emerald-200">
                            <h3 class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest mb-1"><i class="fas fa-check-circle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-emerald-800 font-bold">Certificado</p>
                        </div>`;
                } else if (DashboardState._ledgerTotalCount && DashboardState._ledgerTotalCount > 0) {
                    estadoContainer.innerHTML = `
                        <div class="surgical-card p-4 shadow-sm bg-indigo-50 border-indigo-200">
                            <h3 class="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-1"><i class="fas fa-exclamation-circle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-indigo-800 font-bold">Parcial</p>
                        </div>`;
                } else {
                    estadoContainer.innerHTML = `
                        <div class="surgical-card p-4 shadow-sm bg-slate-50 border-slate-200">
                            <h3 class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1"><i class="fas fa-clock mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-slate-700 font-bold">Pendiente</p>
                        </div>`;
                }"""
new_status = """
                const officialStatus = DashboardState._documentaryStatus || (DashboardState._financialStructure && DashboardState._financialStructure.categories.length > 0 ? "PASS" : "PENDIENTE");
                let colorClass = "bg-slate-50 border-slate-200 text-slate-700";
                if (officialStatus === 'PASS') colorClass = "bg-emerald-50 border-emerald-200 text-emerald-800";
                else if (officialStatus === 'BLOCKED_BY_SOURCE_DATA') colorClass = "bg-amber-50 border-amber-200 text-amber-800";
                else if (officialStatus === 'FAILED' || officialStatus === 'SYSTEM_FAILURE') colorClass = "bg-rose-50 border-rose-200 text-rose-800";
                else if (officialStatus === 'NOT_FOUND' || officialStatus === 'NOT_REQUIRED') colorClass = "bg-indigo-50 border-indigo-200 text-indigo-800";
                
                estadoContainer.innerHTML = `
                    <div class="surgical-card p-4 shadow-sm ${colorClass}">
                        <h3 class="text-[10px] font-bold uppercase tracking-widest mb-1"><i class="fas fa-circle mr-1"></i> Estado del Proceso</h3>
                        <p class="text-lg font-bold">${officialStatus}</p>
                    </div>`;
"""
if old_status in content:
    content = content.replace(old_status, new_status)
    print("Replaced status")
else:
    print("Could not find old_status block")


# Load documentary status in loadDashboard
old_load = """const summary = await ApiClient.getSummary(mp, periodo);"""
new_load = """const summary = await ApiClient.getSummary(mp, periodo);
                try {
                    const certInfo = await ApiClient.safeFetch('/api/v4/dte/certify?marketplace=' + mp + '&periodo=' + periodo);
                    DashboardState._documentaryStatus = certInfo.status_general || 'BLOCKED_BY_SOURCE_DATA';
                } catch(e) {
                    DashboardState._documentaryStatus = 'BLOCKED_BY_SOURCE_DATA';
                }
"""
if old_load in content:
    content = content.replace(old_load, new_load)
    print("Replaced load dashboard")

# Fix Drawer contract mapping
old_drawer = """const d = res.data;
                        document.getElementById('cert-doc-type-text').innerText = d.document_type || '-';
                        document.getElementById('cert-doc-folio-text').innerText = d.folio || '-';
                        
                        const elEmisor = document.getElementById('cert-doc-emisor');
                        if(elEmisor) elEmisor.innerText = d.issuer_tax_id || '-';
                        const elReceptor = document.getElementById('cert-doc-receptor');
                        if(elReceptor) elReceptor.innerText = d.receiver_tax_id || '-';
                        const elFecha = document.getElementById('cert-doc-fecha');
                        if(elFecha) elFecha.innerText = d.issue_date || '-';
                        const elMonto = document.getElementById('cert-doc-monto');
                        if(elMonto) elMonto.innerText = d.total_amount ? `$${d.total_amount.toLocaleString('es-CL')}` : '-';

                        const cert = d.electronic_certificate || {};
                        const pipe = cert.electronic_certificate || {};
                        
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
                        
                        const ev = d.evidence_object || {};
                        document.getElementById('cert-status').innerText = cert.overall_status === 'PASS' ? 'VÁLIDO' : (cert.overall_status || 'INVÁLIDO');
                        document.getElementById('cert-status').className = cert.overall_status === 'PASS' ? 'font-bold text-green-400' : 'font-bold text-red-400';
                        
                        document.getElementById('cert-level').innerText = d.evidence_level || 'DESCONOCIDO';
                        document.getElementById('cert-hash').innerText = ev.evidence_hash ? ev.evidence_hash.substring(0,20) : '-';
                        document.getElementById('ev-hash').innerText = ev.evidence_hash || '-';
                        document.getElementById('ev-conf').innerText = ev.confidence_score ? `${ev.confidence_score}%` : 'N/A';"""

new_drawer = """
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
"""
if old_drawer in content:
    content = content.replace(old_drawer, new_drawer)
    print("Replaced drawer block")
else:
    print("Could not find old drawer block")


content = content.replace("if (res && res.status === 'success' && res.data) {", "if (res && res.document_certification) {")

old_alert = "const complianceAlerts = alerts.filter(a => a.check_name === 'CARGO_SIN_RESPALDO_LEGAL');"
new_alert = "const complianceAlerts = alerts.filter(a => a.check_name === 'CARGO_SIN_RESPALDO_LEGAL' || (a.check_name === 'FOLIO_ESTRUCTURAL_SIN_RESPALDO_SII' && a.marketplace === mp));"
if old_alert in content:
    content = content.replace(old_alert, new_alert)
    print("Replaced alert filter")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved dashboard.html")
