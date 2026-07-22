import re

with open('templates/executive_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Cash flow
cash_flow_replace = """            const cashFlowContainer = document.getElementById('content-cash');
            const cashFlowCards = [];
            
            const cfLabels = {
                "available_balance": "Disponible",
                "releases": "Pendiente por Liberar",
                "holds": "Retenciones",
                "transfers": "Transferencias"
            };
            
            for (const [key, val] of Object.entries(ux12Data.cash_flow)) {
                if (key !== "available_balance" && val === 0) continue;
                const isNeg = val < 0;
                const cls = isNeg ? 'amount-neg' : 'amount-pos';
                const label = cfLabels[key] || key;
                cashFlowCards.push(`<div class="card p-5"><span class="kpi-label">${label}</span><div class="kpi-value ${cls} mt-1">${fmtCLP(val)}</div></div>`);
            }
            
            cashFlowContainer.innerHTML = cashFlowCards.join('');"""

content = re.sub(
    r"const cashFlowContainer = document.getElementById\('content-cash'\);\n            cashFlowContainer\.innerHTML = Object\.entries\(ux12Data\.cash_flow\)\.map.*?\)\.join\(''\);",
    cash_flow_replace,
    content,
    flags=re.DOTALL
)

# Fix 2: AI Narrative
ai_replace = """            // Render AI Narrative
            const aiElem = document.getElementById('ux12-ai-narrative');
            if(aiElem && ux12Data.operational_intelligence.ai_narrative) {
                const paragraphs = ux12Data.operational_intelligence.ai_narrative;
                aiElem.innerHTML = '<i class="fas fa-robot text-indigo-500 mr-2"></i>' + paragraphs.join('<br><br><i class="fas fa-robot text-indigo-500 mr-2"></i>');
            }"""

content = re.sub(
    r"// Render AI Narrative\n            const aiElem = document.getElementById\('ux12-ai-narrative'\);\n            if\(aiElem\) \{\n                aiElem\.innerHTML = '<i class=\"fas fa-robot text-indigo-500 mr-2\"></i>' \+ ux12Data\.ai_narrative;\n            \}",
    ai_replace,
    content,
    flags=re.DOTALL
)

# Fix 3: Also fix the initial URL parameters for `ux12Params` to handle "ALL"
mp_replace = """            const ux12Params = new URLSearchParams();
            if (period !== 'YTD') ux12Params.set('periodo', period);
            if (mp && mp !== 'ALL') ux12Params.set('marketplace', mp);
            const ux12Url = '/api/v4/exec/ux12_summary?' + ux12Params.toString();"""

content = re.sub(
    r"const ux12Params = new URLSearchParams\(\);\n            if \(period !== 'YTD'\) ux12Params\.set\('periodo', period\);\n            if \(mp\) ux12Params\.set\('marketplace', mp\);\n            const ux12Url = '/api/v4/exec/ux12_summary\?' \+ ux12Params\.toString\(\);",
    mp_replace,
    content,
    flags=re.DOTALL
)

with open('templates/executive_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
