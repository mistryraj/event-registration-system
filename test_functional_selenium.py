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

# ---------------------------------------------------------
# 👇 IMPORTANT: I commented this out so you can SEE the browser
# chrome_options.add_argument("--headless=new") 
# ---------------------------------------------------------

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222") 

try:
    # This manager automatically finds the installed Chrome version and downloads the matching driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("http://127.0.0.1:5000")
    time.sleep(2)
    
    # Interaction
    driver.find_element(By.CLASS_NAME, "event-card").click()
    time.sleep(1) # Added small delay for visual demo
    
    driver.find_element(By.ID, "name").send_keys("CI Runner")
    time.sleep(0.5) # Added small delay so typing is visible
    
    driver.find_element(By.ID, "email").send_keys("ci@test.com")
    time.sleep(0.5)
    
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3) # Wait longer at the end so you can see the success message
    
    assert "Registration Successful" in driver.page_source
    print("E2E SELENIUM TEST PASSED!")

except Exception as e:
    print(f"TEST FAILED: {e}")
    sys.exit(1) 

finally:
    if 'driver' in locals():
        driver.quit()