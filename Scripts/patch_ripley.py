import re

def patch_backend():
    with open('api/api.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Allow Ripley to bypass exclude_non_operational since its financial_group is NULL
    old_exclude = 'exclude_clause = "AND financial_group IS NOT NULL" if exclude_non_operational else ""'
    new_exclude = 'exclude_clause = "AND financial_group IS NOT NULL" if exclude_non_operational and marketplace != "RIPLEY" else ""'
    if old_exclude in content:
        content = content.replace(old_exclude, new_exclude)

    with open('api/api.py', 'w', encoding='utf-8') as f:
        f.write(content)

def patch_frontend():
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Dynamically add unmapped categories to blocks
    js_update = """
            const blocks = [
                {id: 'ingresos', title: 'Ingresos Brutos', type: 'positive', data: details.ingresos},
                {id: 'devoluciones', title: 'Devoluciones / Reembolsos', type: 'negative', data: details.devoluciones},
                {id: 'costos_operacionales', title: 'Costos Operacionales y Logísticos', type: 'negative', data: details.costos_operacionales},
                {id: 'costos_comerciales', title: 'Costos Comerciales (Comisiones)', type: 'negative', data: details.costos_comerciales},
                {id: 'ajustes', title: 'Ajustes y Otros', type: 'neutral', data: details.ajustes}
            ];

            // Append any dynamically added categories (like sin_clasificar for Ripley)
            Object.keys(details).forEach(cat => {
                if (!['ingresos', 'devoluciones', 'costos_operacionales', 'costos_comerciales', 'ajustes'].includes(cat) && details[cat] && details[cat].length > 0) {
                    blocks.push({
                        id: cat,
                        title: cat === 'sin_clasificar' ? 'Sin Clasificar (Ripley Data)' : cat.replace('_', ' ').toUpperCase(),
                        type: 'neutral',
                        data: details[cat]
                    });
                }
            });

            let blocksHtml = '';
            blocks.forEach(block => {
                if (!block.data || block.data.length === 0) return;
                
                // Calculate actual sum of the block's data instead of using window._cierreCertified
                // since Ripley's waterfall values are 0
                const actualTotal = block.data.reduce((acc, curr) => acc + curr.total, 0);

                blocksHtml += `
                    <!-- ${block.id.toUpperCase()} -->
                    <div onclick="selectFinancialFilter('category', '${block.id}', '${block.title}')" class="border rounded-xl transition-all duration-200 cursor-pointer ${getCatClasses(block.id)}">
                        <div class="flex justify-between items-end">
                            <span class="text-sm font-bold text-slate-700">${block.title}</span>
                            <span class="${block.type === 'positive' ? 'amount-pos' : block.type === 'negative' ? 'amount-neg' : 'font-mono font-bold'} text-lg">${fmtCLP(actualTotal)}</span>
                        </div>
                        ${renderDetailsHTML(block.data, block.id)}
                    </div>
                `;
            });
            container.innerHTML += blocksHtml;
"""
    
    # We replace the hardcoded HTML blocks inside renderCierre with dynamic iteration
    # Since the HTML is quite long, we'll use regex to replace from `<!-- INGRESOS -->` to the end of `container.innerHTML +=`
    
    # First, let's find where container.innerHTML is assigned for the blocks.
    # It starts with container.innerHTML += `
    # and has <!-- INGRESOS --> inside.
    content = re.sub(r'container\.innerHTML \+= `\s*<!-- INGRESOS -->.*?</div>\s*`;', js_update.strip(), content, flags=re.DOTALL)

    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

patch_backend()
patch_frontend()
