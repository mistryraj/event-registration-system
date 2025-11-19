# test_functional_selenium.py
import time
import threading
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
            db.session.add(Event(title="CI Event", description="Auto", event_date="2025-12-25"))
            db.session.commit()
    app.run(port=5000, use_reloader=False, debug=False, threaded=True)

threading.Thread(target=run_app, daemon=True).start()
time.sleep(5)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.CLASS_NAME, "event-card").click()
    driver.find_element(By.ID, "name").send_keys("CI Runner")
    driver.find_element(By.ID, "email").send_keys("ci@success.com")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    assert "Registration Successful" in driver.page_source
    print("E2E TEST PASSED!")
finally:
    driver.quit()