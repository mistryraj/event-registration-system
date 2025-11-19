# test_functional_selenium.py
import time
import threading
import sys
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
        if Event.query.count() == 0:
            db.session.add(Event(title="Auto Event for CI", description="test", event_date="2025-12-31"))
            db.session.commit()
    # Disable reloader to prevent the thread from spawning duplicates
    app.run(port=5000, use_reloader=False, debug=False)

# Start the Flask app in a separate thread
server_thread = threading.Thread(target=run_app, daemon=True)
server_thread.start()
time.sleep(5)  # Give Flask a moment to start

# --- SELENIUM SETUP ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") # Updated syntax for newer Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222") # Helps in CI environments

try:
    # This manager automatically finds the installed Chrome version and downloads the matching driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("http://127.0.0.1:5000")
    time.sleep(2)
    
    # Interaction
    driver.find_element(By.CLASS_NAME, "event-card").click()
    driver.find_element(By.ID, "name").send_keys("CI Runner")
    driver.find_element(By.ID, "email").send_keys("ci@test.com")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    
    assert "Registration Successful" in driver.page_source
    print("E2E SELENIUM TEST PASSED!")

except Exception as e:
    print(f"TEST FAILED: {e}")
    sys.exit(1) # Ensure the CI pipeline knows it failed

finally:
    if 'driver' in locals():
        driver.quit()