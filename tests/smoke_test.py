from playwright.sync_api import sync_playwright
import time
import sys

def run_smoke_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(f"Console error: {err}"))
        
        def assert_no_nan_or_undefined(html):
            # We look for literal 'NaN' or 'undefined' visible in the DOM
            # Note: Sometimes "undefined" is used in variables, we check visible text mostly
            if '>NaN<' in html or '>NaN</' in html or 'NaN%' in html or '$NaN' in html:
                return False, "Found NaN in DOM"
            if '>undefined<' in html or '>undefined</' in html:
                return False, "Found undefined in DOM"
            return True, ""

        print("=== Running Playwright Smoke Suite ===")

        # 1. Test /app
        print("1. Loading /app")
        page.goto("http://127.0.0.1:3001/app")
        page.wait_for_timeout(3000) # wait for fetches
        html = page.content()
        ok, msg = assert_no_nan_or_undefined(html)
        assert ok, f"/app failed: {msg}"
        print("  [PASS] /app loaded without NaN/undefined")

        # Marketplace Switch on /app
        print("2. Switching Marketplace on /app to PARIS")
        page.select_option("#marketplace-selector", "PARIS")
        page.wait_for_timeout(2000)
        html = page.content()
        ok, msg = assert_no_nan_or_undefined(html)
        assert ok, f"/app MP switch failed: {msg}"
        print("  [PASS] Marketplace switch successful")

        # 3. Test /exec
        print("3. Loading /exec")
        page.goto("http://127.0.0.1:3001/exec")
        page.wait_for_timeout(3000)
        html = page.content()
        ok, msg = assert_no_nan_or_undefined(html)
        assert ok, f"/exec failed: {msg}"
        print("  [PASS] /exec loaded without NaN/undefined")

        # 4. Period Switch on /exec
        print("4. Switching Period on /exec")
        options = page.locator("#exec-period option").all_inner_texts()
        if len(options) > 1:
            page.select_option("#exec-period", index=1)
            page.wait_for_timeout(2000)
            html = page.content()
            ok, msg = assert_no_nan_or_undefined(html)
            assert ok, f"/exec Period switch failed: {msg}"
            print("  [PASS] Period switch successful")
        else:
            print("  [SKIP] Not enough periods to switch")

        # 5. Check Console Errors
        if errors:
            print("  [FAIL] Console errors detected:")
            for e in errors:
                print("    ", e)
            sys.exit(1)
        else:
            print("  [PASS] No console errors detected")

        print("=== All tests passed successfully! ===")
        browser.close()

if __name__ == "__main__":
    run_smoke_test()
