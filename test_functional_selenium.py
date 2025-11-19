import time
import threading
import sys
import os  # <--- Added to check environment
from app import create_app, db, Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        # Ensure we have a test event
        if Event.query.count() == 0:
            db.session.add(Event(title="Auto Event for CI", description="test", event_date="2025-12-31"))
            db.session.commit()
    app.run(port=5000, use_reloader=False, debug=False)

# Start Flask
server_thread = threading.Thread(target=run_app, daemon=True)
server_thread.start()
time.sleep(5)

# --- SMART SELENIUM SETUP ---
chrome_options = Options()

# 🔧 THE FIX: Check if we are running in GitHub Actions (CI)
if os.environ.get('GITHUB_ACTIONS') == 'true':
    print("🤖 CI Environment Detected: Running HEADLESS")
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
else:
    print("👤 Local Environment Detected: Running VISIBLE Browser")
    # We do NOT add headless here, so you can see it!

chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("http://127.0.0.1:5000")
    time.sleep(2)
    
    # Interaction
    driver.find_element(By.CLASS_NAME, "event-card").click()
    time.sleep(1)
    driver.find_element(By.ID, "name").send_keys("CI Runner")
    driver.find_element(By.ID, "email").send_keys("ci@test.com")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    
    assert "Registration Successful" in driver.page_source
    print("✅ E2E SELENIUM TEST PASSED!")

except Exception as e:
    print(f"❌ TEST FAILED: {e}")
    sys.exit(1)

finally:
    if 'driver' in locals():
        driver.quit()