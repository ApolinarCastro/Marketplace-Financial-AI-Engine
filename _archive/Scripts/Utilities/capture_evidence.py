from playwright.sync_api import sync_playwright
import time

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        # Go to app
        page.goto("http://127.0.0.1:8003/app")
        time.sleep(2)
        
        # Select Paris
        page.locator("select#marketplaceSelect").select_option("PARIS")
        time.sleep(1)
        
        # Select Ene-2026
        page.locator("select#periodoSelect").select_option("2026-01")
        time.sleep(2)
        
        # 1. Capture DevTools/Network equivalent: screenshot of the general view 
        # (Though we already have the JSON, let's take a screenshot of the base summary)
        page.screenshot(path="C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/485c7e15-2ea0-4042-be6c-7ebb94590986/scratch/1_API_SUMMARY_PARIS_2026_01.png")
        print("Captured 1_API_SUMMARY_PARIS_2026_01.png")
        
        # 2. Click en Venta
        # Wait for waterfall to load
        time.sleep(1)
        
        # Click the row in the waterfall where concept is "Venta"
        # The frontend seems to use buttons or table rows. Let's find text "Venta"
        try:
            venta_row = page.locator("td:has-text('Venta')").first
            venta_row.click(force=True)
            time.sleep(2)
            
            # Screenshot of Venta clicked
            page.screenshot(path="C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/485c7e15-2ea0-4042-be6c-7ebb94590986/scratch/2_CLICK_EN_VENTA.png")
            print("Captured 2_CLICK_EN_VENTA.png")
        except Exception as e:
            print("Could not click Venta:", e)
            
        browser.close()

if __name__ == "__main__":
    capture()
