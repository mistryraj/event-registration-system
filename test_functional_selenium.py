# test_functional_selenium.py
import time
import threading
from app import create_app, db, Event
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Start Flask app in background
def run_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5000, use_reloader=False, debug=False, threaded=True)

threading.Thread(target=run_app, daemon=True).start()
time.sleep(4)  # Give server time to start

# Headless Chrome (perfect for GitHub Actions)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://127.0.0.1:5000")
    print("Opened student dashboard")

    # Auto-create one event if none exists
    app = create_app()
    with app.app_context():
        if Event.query.count() == 0:
            db.session.add(Event(title="CI Test Event", description="Auto-created", event_date="2025-12-25"))
            db.session.commit()

    driver.refresh()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "event-card").click()
    print("Clicked event card")

    driver.find_element(By.ID, "name").send_keys("GitHub CI User")
    driver.find_element(By.ID, "email").send_keys("ci@example.com")
    driver.find_element(By.TAG_NAME, "button").click()
    print("Submitted registration")

    time.sleep(2)
    h1_text = driver.find_element(By.TAG_NAME, "h1").text
    assert "Registration Successful" in h1_text
    print("E2E TEST PASSED SUCCESSFULLY!")

except Exception as e:
    print(f"E2E TEST FAILED: {e}")
    raise

finally:
    driver.quit()