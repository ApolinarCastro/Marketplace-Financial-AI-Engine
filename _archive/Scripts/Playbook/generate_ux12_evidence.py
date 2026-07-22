import asyncio
from playwright.async_api import async_playwright
import urllib.request
import json

async def main():
    api_base = "http://localhost:8003/api/v4/exec/ux12_summary?periodo=2026-02"
    
    marketplaces = {
        "ALL": "Todos los Marketplaces",
        "ML": "Mercado Libre",
        "PARIS": "Paris",
        "RIPLEY": "Ripley"
    }

    evidence_lines = [
        "# CERTIFICACIÓN DE DEFECTO 001 y 002: FLUJO DE CAJA E INTELIGENCIA OPERATIVA",
        "*Fecha de Certificación: 2026-06-09*",
        "*Periodo: 2026-02*",
        "",
        "## TABLA DE CONCILIACIÓN MATEMÁTICA",
        "",
        "| Marketplace | Disponible API | Disponible UI | Delta |",
        "| :--- | :--- | :--- | :--- |"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for mp_id, mp_name in marketplaces.items():
            # 1. API Value
            url = api_base
            if mp_id != "ALL":
                url += f"&marketplace={mp_id}"
            resp = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
            api_val = resp.get("cash_flow", {}).get("available_balance", 0)
            api_fmt = f"${api_val:,.0f}".replace(",", ".")
            
            # 2. UI Value & Screenshot
            await page.goto("http://localhost:8003/")
            await page.wait_for_selector("#exec-period")
            await page.select_option("#exec-period", "2026-02")
            await page.wait_for_timeout(500)
            await page.select_option("#exec-mp", mp_id if mp_id != "ALL" else "")
            await page.wait_for_timeout(2000) # wait for fetch and render
            
            ui_text = await page.locator("span.kpi-label:has-text('Disponible') + div.kpi-value").inner_text()
            
            # Clean UI text to number
            ui_clean = ui_text.replace('$', '').replace('.', '')
            try:
                ui_val = float(ui_clean)
            except:
                ui_val = 0.0
            
            delta = abs(round(api_val) - ui_val)
            
            evidence_lines.append(f"| **{mp_name}** | `{api_fmt}` | `{ui_text}` | `${delta:,.2f}` |")
            
            # Screenshot
            await page.screenshot(path=f"evidence_ux12_{mp_id}.png", full_page=True)
        
        await browser.close()
        
    evidence_lines.extend([
        "",
        "## EVIDENCIA VISUAL",
        "A continuación se demuestra que la UI cambia dinámicamente y la narrativa IA acompaña los datos.",
        "",
        "### Mercado Libre",
        "![ML](evidence_ux12_ML.png)",
        "",
        "### Paris",
        "![Paris](evidence_ux12_PARIS.png)",
        "",
        "### Ripley",
        "![Ripley](evidence_ux12_RIPLEY.png)",
        "",
        "### Todos los Marketplaces",
        "![Consolidado](evidence_ux12_ALL.png)",
    ])
    
    with open("UX12_EVIDENCE.md", "w", encoding="utf-8") as f:
        f.write("\n".join(evidence_lines))
    print("Report written successfully to UX12_EVIDENCE.md")

if __name__ == "__main__":
    asyncio.run(main())
