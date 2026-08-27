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
        
        await page.wait_for_function('() => document.querySelector("#exec-period").options.length > 1')
        
        # Test FALABELLA 2026-05
        await page.select_option('#exec-mp', 'FALABELLA')
        await page.wait_for_timeout(1000)
        await page.select_option('#exec-period', '2026-05')
        await page.wait_for_timeout(3000)
        
        print('=== Executive Dashboard - Falabella 2026-05 ===')
        
        header_badge = await page.text_content('#audit-status-badge')
        print('Header audit status badge:', header_badge[:200] if header_badge else 'EMPTY')
        
        audit_section = await page.text_content('#audit-status')
        print('Audit status section:', audit_section[:500] if audit_section else 'EMPTY')
        
        # Test RIPLEY
        await page.select_option('#exec-mp', 'RIPLEY')
        await page.wait_for_timeout(1000)
        await page.select_option('#exec-period', '2026-05')
        await page.wait_for_timeout(3000)
        
        print('\n=== Executive Dashboard - Ripley 2026-05 ===')
        
        header_badge = await page.text_content('#audit-status-badge')
        print('Header audit status badge:', header_badge[:200] if header_badge else 'EMPTY')
        
        audit_section = await page.text_content('#audit-status')
        print('Audit status section:', audit_section[:500] if audit_section else 'EMPTY')
        
        # Test ML
        await page.select_option('#exec-mp', 'ML')
        await page.wait_for_timeout(1000)
        await page.select_option('#exec-period', '2026-05')
        await page.wait_for_timeout(3000)
        
        print('\n=== Executive Dashboard - ML 2026-05 ===')
        
        header_badge = await page.text_content('#audit-status-badge')
        print('Header audit status badge:', header_badge[:200] if header_badge else 'EMPTY')
        
        audit_section = await page.text_content('#audit-status')
        print('Audit status section:', audit_section[:500] if audit_section else 'EMPTY')
        
        # Test PARIS
        await page.select_option('#exec-mp', 'PARIS')
        await page.wait_for_timeout(1000)
        await page.select_option('#exec-period', '2026-05')
        await page.wait_for_timeout(3000)
        
        print('\n=== Executive Dashboard - Paris 2026-05 ===')
        
        header_badge = await page.text_content('#audit-status-badge')
        print('Header audit status badge:', header_badge[:200] if header_badge else 'EMPTY')
        
        audit_section = await page.text_content('#audit-status')
        print('Audit status section:', audit_section[:500] if audit_section else 'EMPTY')
        
        await browser.close()

asyncio.run(test())