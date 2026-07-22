import re

with open("templates/executive_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

new_main = """
    <main class="p-8 max-w-7xl mx-auto space-y-6 fade-in">
        
        <!-- FASE 4: Distribution by Marketplace (P3: Ventas/Devoluciones/Cobros/Disponible) -->
        <section id="scorecard">
            <h2 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Distribución por Marketplace</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5" id="scorecard-grid">
            </div>
        </section>

        <!-- P1: Estado Auditoría -->
        <section id="audit-status" class="card p-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span>
                <span class="text-xs font-bold text-slate-700">Estado Auditoría</span>
                <span class="pill bg-emerald-100 text-emerald-700 text-[9px] font-bold px-2 py-0.5 rounded-full">Certificado</span>
            </div>
            <a href="/app" class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 px-3 py-1.5 rounded-lg transition-all">
                <i class="fas fa-external-link-alt mr-1.5"></i>Ver Auditoría
            </a>
        </section>

        <!-- CAPA OPERACIONAL -->
        <section class="mt-8">
            <h2 class="text-lg font-bold text-slate-800 mb-4">Capa Operacional (Seller + Fulfillment)</h2>
            <div class="grid grid-cols-2 lg:grid-cols-5 gap-5">
                <div class="card p-5"><span class="kpi-label">Venta MP</span><div class="kpi-value amount-pos mt-1" id="v3-op-venta-mp">—</div></div>
                <div class="card p-5"><span class="kpi-label">Venta FF</span><div class="kpi-value amount-pos mt-1" id="v3-op-venta-ff">—</div></div>
                <div class="card p-5"><span class="kpi-label">Venta Consolidada</span><div class="kpi-value amount-pos mt-1" id="v3-op-venta-cons">—</div></div>
                <div class="card p-5"><span class="kpi-label">Órdenes MP</span><div class="kpi-value mt-1 text-slate-800" id="v3-op-ord-mp">—</div></div>
                <div class="card p-5"><span class="kpi-label">Órdenes FF</span><div class="kpi-value mt-1 text-slate-800" id="v3-op-ord-ff">—</div></div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
                <!-- Waterfall Operacional -->
                <section class="lg:col-span-12 card p-6 lg:p-8">
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h2 class="text-xs font-bold text-slate-400 uppercase tracking-widest">Waterfall Operacional</h2>
                            <p class="text-[12px] text-slate-500 mt-0.5 font-medium" id="v3-wf-op-subtitle">Cargando...</p>
                        </div>
                    </div>
                    <div id="v3-wf-op-bars" class="space-y-2"></div>
                </section>
            </div>
        </section>

        <!-- CAPA LIQUIDACIÓN -->
        <section class="mt-8">
            <h2 class="text-lg font-bold text-slate-800 mb-4">Capa Liquidación (Ciclos de Facturación)</h2>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-5">
                <div class="card p-5"><span class="kpi-label">Subtotal Liquidado</span><div class="kpi-value amount-pos mt-1" id="v3-liq-venta">—</div></div>
                <div class="card p-5"><span class="kpi-label">Comisiones</span><div class="kpi-value amount-neg mt-1" id="v3-liq-com">—</div></div>
                <div class="card p-5"><span class="kpi-label">Ajustes</span><div class="kpi-value amount-neg mt-1" id="v3-liq-aj">—</div></div>
                <div class="card p-5 bg-gradient-to-br from-indigo-600 to-indigo-800 text-white shadow-lg"><span class="kpi-label text-indigo-200">Pago Neto</span><div class="kpi-value-primary mt-1" id="v3-liq-neto">—</div></div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
                <!-- Waterfall Liquidacion -->
                <section class="lg:col-span-12 card p-6 lg:p-8">
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h2 class="text-xs font-bold text-slate-400 uppercase tracking-widest">Waterfall Liquidación</h2>
                            <p class="text-[12px] text-slate-500 mt-0.5 font-medium" id="v3-wf-liq-subtitle">Cargando...</p>
                        </div>
                    </div>
                    <div id="v3-wf-liq-bars" class="space-y-2"></div>
                </section>
            </div>
        </section>

        <!-- CAPA TESORERÍA -->
        <section class="mt-8">
            <h2 class="text-lg font-bold text-slate-800 mb-4">Capa Tesorería (Bancos)</h2>
            <div class="grid grid-cols-2 lg:grid-cols-3 gap-5">
                <div class="card p-5"><span class="kpi-label">Disponible</span><div class="kpi-value amount-pos mt-1" id="v3-tes-disp">—</div></div>
                <div class="card p-5"><span class="kpi-label">Transferencias</span><div class="kpi-value amount-pos mt-1" id="v3-tes-trans">—</div></div>
                <div class="card p-5"><span class="kpi-label">Pagos Recibidos</span><div class="kpi-value amount-pos mt-1" id="v3-tes-pagos">—</div></div>
            </div>
        </section>

        <h2 class="text-lg font-bold text-slate-800 mb-4 mt-8">Cobertura Documental (DTE)</h2>
        <p id="dte-explanation" class="text-xs text-slate-500 mb-4 hidden">Matching tributario no certificable con evidencia actual.</p>
        <div id="content-doc" class="grid grid-cols-2 lg:grid-cols-4 gap-5">
            <div class="card p-5"><span class="kpi-label">XML Conciliados</span><div class="kpi-value text-slate-800 mt-1" id="ux12-doc-match">—</div></div>
            <div class="card p-5"><span class="kpi-label">XML Pendientes</span><div class="kpi-value text-slate-800 mt-1" id="ux12-doc-pend">—</div></div>
            <div class="card p-5"><span class="kpi-label">Total DTE Asociados</span><div class="kpi-value text-slate-800 mt-1" id="ux12-doc-total">—</div></div>
            <div class="card p-5 bg-slate-800 text-white shadow-lg"><span class="kpi-label text-slate-300">Cobertura</span><div class="kpi-value-primary mt-1" id="ux12-doc-cov">—</div></div>
        </div>

    </main>
"""

new_script = """
        // ── Main Load V3 ──
        async function loadExecutiveDashboard() {
            const period = document.getElementById('exec-period').value;
            const mp = document.getElementById('exec-mp').value;
            
            // For scorecard and documentary we still fetch the old summary, because we didn't rewrite the scorecard logic yet in v3
            const summaryUrl = '/api/v4/exec/summary' + (period !== 'YTD' ? '?periodo=' + period : '');
            
            // For the new V3 KPIs
            const v3Params = new URLSearchParams();
            if (period !== 'YTD') v3Params.set('periodo', period);
            if (mp && mp !== 'ALL') v3Params.set('marketplace', mp);
            const v3Url = '/api/v4/exec/summary-v3?' + v3Params.toString();

            const [summaryRes, v3Res] = await Promise.all([fetch(summaryUrl), fetch(v3Url)]);
            
            let summary = { total_gross_revenue: 0, total_devoluciones: 0, total_cobros: 0, total_net_revenue: 0, marketplaces: [] };
            if (summaryRes.ok) summary = await summaryRes.json();
            
            let v3Data = null;
            if (v3Res.ok) v3Data = await v3Res.json();

            if (v3Data) {
                // Operacional
                document.getElementById('v3-op-venta-mp').textContent = fmtCLP(v3Data.operacional.venta_mp);
                document.getElementById('v3-op-venta-ff').textContent = fmtCLP(v3Data.operacional.venta_ff);
                document.getElementById('v3-op-venta-cons').textContent = fmtCLP(v3Data.operacional.venta_operacional_consolidada);
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
            
            // Populate Alert Status
            let alerts = summary.total_alert_count || 0;
            if (mp && mp !== 'ALL') {
                const target = summary.marketplaces.find(m => m.id === mp);
                if (target) alerts = target.alert_count || 0;
            }
            
            const badgeHeader = document.getElementById('audit-status-badge');
            const taxBadgeHeader = document.getElementById('tax-status-badge');
            const dteExpl = document.getElementById('dte-explanation');
            const auditText = document.getElementById('audit-text');
            const badgeSection = document.getElementById('audit-status');
            
            if (mp === 'RIPLEY') {
                if (taxBadgeHeader) taxBadgeHeader.classList.remove('hidden');
                if (dteExpl) dteExpl.classList.remove('hidden');
                if (badgeHeader) {
                    badgeHeader.innerHTML = '<span class="w-2 h-2 bg-emerald-500 rounded-full"></span>Financiero: PRE_LOCK CERTIFICADO';
                    badgeHeader.className = 'flex items-center gap-1.5 text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg px-2.5 py-1.5';
                }
                if (auditText) {
                    auditText.classList.remove('hidden');
                    auditText.textContent = (alerts > 0) ? alerts + ' anomalías operacionales' : 'Sin alertas visibles';
                }
                if (badgeSection) {
                    badgeSection.innerHTML = `
                        <div class="flex items-center gap-3">
                            <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span>
                            <span class="text-xs font-bold text-slate-700">Estado Auditoría</span>
                            <span class="pill bg-emerald-100 text-emerald-700 text-[9px] font-bold px-2 py-0.5 rounded-full">Financiero: PRE_LOCK</span>
                        </div>
                        <a href="/app" class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 px-3 py-1.5 rounded-lg transition-all">
                            <i class="fas fa-external-link-alt mr-1.5"></i>Ver Auditoría
                        </a>
                    `;
                }
            } else {
                if (taxBadgeHeader) taxBadgeHeader.classList.add('hidden');
                if (dteExpl) dteExpl.classList.add('hidden');
                
                if (alerts > 0) {
                    if(badgeHeader) {
                        badgeHeader.innerHTML = '<span class="w-2 h-2 bg-rose-500 rounded-full animate-pulse"></span>Alertas Activas';
                        badgeHeader.className = 'flex items-center gap-1.5 text-[11px] font-semibold text-rose-700 bg-rose-50 border border-rose-200 rounded-lg px-2.5 py-1.5';
                    }
                    if (auditText) {
                        auditText.classList.remove('hidden');
                        auditText.textContent = alerts + ' anomalías operacionales';
                    }
                    if(badgeSection) {
                        badgeSection.innerHTML = `
                            <div class="flex items-center gap-3">
                                <span class="w-2.5 h-2.5 bg-rose-500 rounded-full animate-pulse"></span>
                                <span class="text-xs font-bold text-slate-700">Estado Auditoría</span>
                                <span class="pill bg-rose-100 text-rose-700 text-[9px] font-bold px-2 py-0.5 rounded-full">Alerta de Revisión</span>
                            </div>
                            <a href="/app" class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 px-3 py-1.5 rounded-lg transition-all">
                                <i class="fas fa-external-link-alt mr-1.5"></i>Resolver ${alerts} alertas
                            </a>
                        `;
                    }
                } else {
                    if(badgeHeader) {
                        badgeHeader.innerHTML = '<span class="w-2 h-2 bg-emerald-500 rounded-full"></span>Certificado';
                        badgeHeader.className = 'flex items-center gap-1.5 text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg px-2.5 py-1.5';
                    }
                    if (auditText) {
                        auditText.classList.remove('hidden');
                        auditText.textContent = 'Sin alertas visibles';
                    }
                    if(badgeSection) {
                        badgeSection.innerHTML = `
                            <div class="flex items-center gap-3">
                                <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span>
                                <span class="text-xs font-bold text-slate-700">Estado Auditoría</span>
                                <span class="pill bg-emerald-100 text-emerald-700 text-[9px] font-bold px-2 py-0.5 rounded-full">Certificado</span>
                            </div>
                            <a href="/app" class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 px-3 py-1.5 rounded-lg transition-all">
                                <i class="fas fa-external-link-alt mr-1.5"></i>Ver Auditoría
                            </a>
                        `;
                    }
                }
            }

            // Scorecard
            const grid = document.getElementById('scorecard-grid');
            const mpNames = { ML: 'Mercado Libre', RIPLEY: 'Ripley', PARIS: 'Paris', FALABELLA: 'Falabella' };
            const selectedMp = mp || '';

            let leaderId = '';
            let maxNet = -Infinity;
            summary.marketplaces.forEach(m => {
                if (m.net_revenue > maxNet) { maxNet = m.net_revenue; leaderId = m.id; }
            });

            grid.innerHTML = summary.marketplaces.map(mpItem => {
                const name = mpNames[mpItem.id] || mpItem.id;
                const gross = mpItem.gross_revenue;
                const dev = mpItem.devoluciones || 0;
                const cob = mpItem.cobros || 0;
                const net = mpItem.net_revenue;
                const isSelected = selectedMp && selectedMp === mpItem.id;
                const isLeader = mpItem.id === leaderId && leaderId !== '';
                const isInactive = gross === 0 && net === 0;
                let activeClass = isSelected ? 'ring-2 ring-indigo-500 shadow-md' : '';
                if (isInactive) activeClass += ' opacity-60';

                if (isInactive) {
                    return `
                        <div class="card p-5 scorecard ${activeClass}">
                            <div class="flex justify-between items-start mb-2">
                                <span class="text-xs font-bold text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">${name}</span>
                            </div>
                            <div class="py-4 text-center">
                                <span class="text-[10px] font-semibold text-slate-400 bg-slate-100 px-3 py-1.5 rounded-full inline-block">
                                    <i class="fas fa-pause-circle mr-1.5"></i>Sin actividad en el período
                                </span>
                            </div>
                        </div>
                    `;
                }

                return `
                    <div class="card p-5 scorecard cursor-pointer ${activeClass}" onclick="selectMarketplace('${mpItem.id}')">
                        <div class="flex justify-between items-start mb-3">
                            <span class="text-xs font-bold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-lg">${name}
                                ${isLeader ? ' <span class="text-amber-500 ml-1">🏆</span>' : ''}
                            </span>
                            <span class="flex items-center gap-1.5">
                                ${isLeader ? '<span class="text-[9px] font-bold text-amber-600 bg-amber-50 border border-amber-200 px-1.5 py-0.5 rounded">Mayor aporte</span>' : ''}
                                <span class="text-[10px] text-slate-400 font-medium">${fmtCLP(net)} disp.</span>
                            </span>
                        </div>
                        <div class="space-y-1.5">
                            <div class="flex justify-between items-center">
                                <span class="kpi-label" title="Valor bruto de ventas del período">Venta Bruta</span>
                                <span class="text-sm font-bold text-slate-800">${fmtCLP(mpItem.venta_bruta)}</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="kpi-label">Devoluciones</span>
                                <span class="text-sm font-bold ${dev >= 0 ? 'amount-pos' : 'amount-neg'}">${fmtCLP(dev)}</span>
                            </div>
                            <div class="flex justify-between items-center" title="Comisiones + Costos Operacionales. Ver detalle en panel inferior.">
                                <span class="kpi-label">Costos & Comisiones</span>
                                <span class="text-sm font-bold ${cob >= 0 ? 'amount-pos' : 'amount-neg'}">${fmtCLP(cob)}</span>
                            </div>
                            <div class="flex justify-between items-center pt-2 border-t border-slate-100">
                                <span class="kpi-label">Disponible</span>
                                <span class="text-sm font-bold ${net >= 0 ? 'amount-pos' : 'amount-neg'}">${fmtCLP(net)}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');

            await loadWaterfallV3();
        }

        async function loadWaterfallV3() {
            const period = document.getElementById('exec-period').value;
            const mp = document.getElementById('exec-mp').value;
            const params = new URLSearchParams();
            if (mp) params.set('marketplace', mp);
            if (period !== 'YTD') params.set('periodo', period);

            const res = await fetch('/api/v4/exec/waterfall-v3?' + params.toString());
            const data = await res.json();

            const mpLabel = data.marketplace === 'ALL' ? 'Consolidado' : data.marketplace;
            document.getElementById('v3-wf-op-subtitle').textContent = mpLabel + ' · ' + (period !== 'YTD' ? period : 'YTD');
            document.getElementById('v3-wf-liq-subtitle').textContent = mpLabel + ' · ' + (period !== 'YTD' ? period : 'YTD');

            // Render Op Waterfall
            const opData = data.operacional;
            const maxValOp = Math.max(...opData.values.map(Math.abs), Math.abs(opData.neto));
            renderWaterfallBars('v3-wf-op-bars', opData.labels, opData.values, opData.neto, maxValOp);

            // Render Liq Waterfall
            const liqData = data.liquidacion;
            const maxValLiq = Math.max(...liqData.values.map(Math.abs), Math.abs(liqData.neto));
            renderWaterfallBars('v3-wf-liq-bars', liqData.labels, liqData.values, liqData.neto, maxValLiq);
        }

        function renderWaterfallBars(containerId, labels, values, neto, maxVal) {
            const container = document.getElementById(containerId);
            let html = '';
            
            // Build steps list
            const steps = [];
            values.forEach((v, i) => {
                steps.push({
                    label: labels[i],
                    value: v,
                    color: v < 0 ? 'bg-rose-400' : 'bg-emerald-500',
                    pct: maxVal === 0 ? 0 : Math.min(100, (Math.abs(v) / maxVal) * 100)
                });
            });
            steps.push({
                label: 'Resultado Neto',
                value: neto,
                color: 'bg-blue-600',
                pct: maxVal === 0 ? 0 : Math.min(100, (Math.abs(neto) / maxVal) * 100)
            });

            steps.forEach((s, i) => {
                const isNeg = s.value < 0;
                const cls = isNeg ? 'amount-neg' : (s.label === 'Resultado Neto' ? 'text-blue-700 font-bold' : 'amount-pos');

                if (i > 0) {
                    html += `<div class="arrow-flow"><i class="fas fa-arrow-down text-slate-300 text-[10px]"></i></div>`;
                }

                html += `
                    <div class="waterfall-step">
                        <div class="flex justify-between text-sm mb-1">
                            <span class="font-semibold text-slate-700">${s.label}</span>
                            <span class="${cls} font-mono text-sm">${fmtCLP(s.value)}</span>
                        </div>
                        <div class="flex w-full bg-slate-100 rounded-lg h-7 overflow-hidden shadow-inner">
                            ${isNeg
                                ? `<div class="h-full rounded-r-lg ${s.color} opacity-80" style="width: ${s.pct}%"></div><div class="flex-1"></div>`
                                : `<div class="flex-1"></div><div class="h-full rounded-l-lg ${s.color}" style="width: ${s.pct}%"></div>`
                            }
                        </div>
                        <div class="flex justify-between text-[10px] text-slate-400 mt-0.5 px-0.5">
                            <span>${isNeg ? '-$' + fmtShort(Math.abs(s.value)) : fmtShort(s.value)}</span>
                            <span>${s.pct.toFixed(0)}% ref.</span>
                        </div>
                    </div>
                `;
            });

            container.innerHTML = html;
        }
"""

content = re.sub(r'<main.*?</main>', new_main, content, flags=re.DOTALL)

script_start = content.find('async function loadExecutiveDashboard() {')
if script_start != -1:
    # We replace from loadExecutiveDashboard to the bottom before </script>
    script_end = content.rfind('</script>')
    old_script_chunk = content[script_start:script_end]
    content = content.replace(old_script_chunk, new_script + "\n        // ── Init ──\n        loadExecutiveDashboard();\n    ")

with open("templates/executive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)
