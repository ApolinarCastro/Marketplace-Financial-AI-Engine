import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on('console', lambda msg: print(f'CONSOLE: {msg.text}'))
        page.on('pageerror', lambda err: print(f'ERROR: {err}'))
        
        # Test executive dashboard
        await page.goto('http://127.0.0.1:3001/exec')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        # Wait for periods
        await page.wait_for_function('() => document.querySelector("#exec-period").options.length > 1')
        
        # Select Falabella
        await page.select_option('#exec-mp', 'FALABELLA')
        await page.wait_for_timeout(1000)
        
        # Select 2026-05
        await page.select_option('#exec-period', '2026-05')
        await page.wait_for_timeout(3000)
        
        print('=== Executive Dashboard - Falabella 2026-05 ===')
        
        # Check audit status badge in header
        header_badge = await page.text_content('#audit-status-badge')
        print('Header audit status badge:', header_badge[:200] if header_badge else 'EMPTY')
        
        # Check audit status section
        audit_section = await page.text_content('#audit-status')
        print('Audit status section:', audit_section[:500] if audit_section else 'EMPTY')
        
        # Test running audit
        print('\n--- Running Audit ---')
        await page.goto('http://127.0.0.1:3001/app')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        await page.wait_for_function('() => document.querySelector("#period-selector").options.length > 1')
        
        await page.select_option('#marketplace-selector', 'FALABELLA')
        await page.wait_for_timeout(1000)
        await page.wait_for_function('() => document.querySelector("#period-selector").options.length > 1')
        
        periods = await page.eval_on_selector('#period-selector', 'el => Array.from(el.options).map(o => o.value)')
        target_period = '2026-05' if '2026-05' in periods else periods[0]
        await page.select_option('#period-selector', target_period)
        await page.wait_for_timeout(3000)
        
        # Get certification status before audit
        estado_before = await page.text_content('#estado-proceso-container')
        print('Certification before audit:', estado_before[:200] if estado_before else 'EMPTY')
        
        # Click run audit button
        await page.click('button:has-text("Ejecutar Auditoría")')
        await page.wait_for_timeout(10000)  # Wait for audit to complete
        
        # Get certification status after audit
        estado_after = await page.text_content('#estado-proceso-container')
        print('Certification after audit:', estado_after[:200] if estado_after else 'EMPTY')
        
        audit_status = await page.text_content('#audit-execution-status')
        print('Audit execution status after audit:', audit_status[:200] if audit_status else 'EMPTY')
        
        await browser.close()

asyncio.run(test())