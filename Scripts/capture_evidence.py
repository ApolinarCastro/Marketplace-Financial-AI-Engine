import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

def capture_evidence():
    # Start the server
    server_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.api:app", "--port", "8000"])
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Create artifacts directory if needed
            artifacts_dir = os.path.join(os.path.expanduser('~'), '.gemini', 'antigravity-ide', 'brain', 'e82ad090-f7e0-4ec9-8538-f4dda9f4cd37')
            os.makedirs(artifacts_dir, exist_ok=True)

            for mp in ['RIPLEY', 'ML', 'PARIS']:
                print(f"Capturing evidence for {mp}...")
                page.goto(f"http://127.0.0.1:8000/")
                page.wait_for_selector("#marketplace-selector")
                page.select_option("#marketplace-selector", value=mp)
                page.click("button:has-text('Ejecutar Auditoría')")
                
                # Wait for structural components to load
                page.wait_for_selector("#estructura-financiera-panel")
                time.sleep(2) # Give it extra time for renderCierre to finish
                
                img_path = os.path.join(artifacts_dir, f"evidence_{mp.lower()}.png")
                page.locator("#estructura-financiera-panel").screenshot(path=img_path)
                print(f"Saved {img_path}")
            
            browser.close()
    finally:
        server_process.terminate()

if __name__ == '__main__':
    capture_evidence()
