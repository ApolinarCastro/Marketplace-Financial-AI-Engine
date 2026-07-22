import re

path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the renderCierre function block completely
target = """            // FASE 2 & FIX-005: ESTADO DEL PROCESO independiente (Standardize status)
            if (estadoContainer) {
                estadoContainer.classList.remove('hidden');
                const isCertified = window._financialStructure && window._financialStructure.categories && window._financialStructure.categories.length > 0;
                const statusName = DashboardState._documentaryStatus || (isCertified ? "PASS" : "PENDING");

                let badgeHtml = '';
                if (statusName === 'VALIDATED' || statusName === 'PASS') {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-emerald-50 border-emerald-200">
                            <h3 class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest mb-1"><i class="fas fa-check-circle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-emerald-800 font-bold">${statusName}</p>
                        </div>`;
                } else if (statusName === 'BLOCKED_BY_SOURCE_DATA' || statusName === 'MISSING_SETTLEMENT') {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-amber-50 border-amber-200">
                            <h3 class="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-1"><i class="fas fa-exclamation-triangle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-amber-800 font-bold">${statusName}</p>
                        </div>`;
                } else {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-indigo-50 border-indigo-200">
                            <p class="text-lg text-indigo-800 font-bold">${statusName}</p>
                        </div>`;
                }
                estadoContainer.innerHTML = badgeHtml;
            }"""

replacement = """            // FASE 2 & FIX-005: ESTADO DEL PROCESO independiente (Standardize status)
            if (estadoContainer) {
                estadoContainer.classList.remove('hidden');
                const isCertified = window._financialStructure && window._financialStructure.categories && window._financialStructure.categories.length > 0;
                const statusName = DashboardState._documentaryStatus || (isCertified ? "VALIDATED" : "PENDING");

                let badgeHtml = '';
                if (statusName === 'VALIDATED' || statusName === 'PASS') {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-emerald-50 border-emerald-200">
                            <h3 class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest mb-1"><i class="fas fa-check-circle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-emerald-800 font-bold">${statusName}</p>
                        </div>`;
                } else if (statusName === 'BLOCKED_BY_SOURCE_DATA' || statusName === 'MISSING_SETTLEMENT') {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-amber-50 border-amber-200">
                            <h3 class="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-1"><i class="fas fa-exclamation-triangle mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-amber-800 font-bold">${statusName}</p>
                        </div>`;
                } else {
                    badgeHtml = `
                        <div class="surgical-card p-4 shadow-sm bg-indigo-50 border-indigo-200">
                            <h3 class="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-1"><i class="fas fa-clock mr-1"></i> Estado del Proceso</h3>
                            <p class="text-lg text-indigo-800 font-bold">${statusName}</p>
                        </div>`;
                }
                estadoContainer.innerHTML = badgeHtml;
            }"""

content = content.replace(target, replacement)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed renderCierre block")
