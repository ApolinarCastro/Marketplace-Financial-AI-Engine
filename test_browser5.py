import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on('console', lambda msg: print(f'CONSOLE: {msg.text}'))
        page.on('pageerror', lambda err: print(f'ERROR: {err}'))
        
        await page.goto('http://127.0.0.1:3001/app')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        await page.wait_for_function('() => document.querySelector("#period-selector").options.length > 1')
        
        # Test FALABELLA 2026-04
        await page.select_option('#marketplace-selector', 'FALABELLA')
        await page.wait_for_timeout(1000)
        await page.wait_for_function('() => document.querySelector("#period-selector").options.length > 1')
        
        await page.select_option('#period-selector', '2026-04')
        await page.wait_for_timeout(3000)
        
        print('=== Falabella 2026-04 ===')
        
        estado = await page.text_content('#estado-proceso-container')
        print('Estado proceso container:', estado[:500] if estado else 'EMPTY')
        
        audit_status = await page.text_content('#audit-execution-status')
        print('Audit execution status:', audit_status[:500] if audit_status else 'EMPTY')
        
        dte_status = await page.text_content('#dte-chain-status')
        print('DTE chain status:', dte_status[:500] if dte_status else 'EMPTY')
        
        # Hard reload test
        print('\n=== Hard Reload Test (Falabella 2026-05) ===')
        await page.select_option('#marketplace-selector', 'FALABELLA')
        await page.wait_for_timeout(1000)
        await page.select_option('#period-selector', '2026-05')
        await page.wait_for_timeout(3000)
        
        await page.reload()
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        await page.wait_for_function('() => document.querySelector("#period-selector").options.length > 1')
        await page.select_option('#marketplace-selector', 'FALABELLA')
        await page.wait_for_timeout(1000)
        await page.select_option('#period-selector', '2026-05')
        await page.wait_for_timeout(3000)
        
        estado = await page.text_content('#estado-proceso-container')
        print('Estado proceso container (after hard reload):', estado[:500] if estado else 'EMPTY')
        
        await browser.close()

asyncio.run(test())