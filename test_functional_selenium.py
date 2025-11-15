import time
import threading
from app import create_app
from selenium import webdriver
# --- NEW: Import the Service class ---
from selenium.webdriver.chrome.service import Service

# --- IMPORTANT: CHANGE THIS ---
# Make sure this matches the driver file you downloaded
DRIVER_PATH = './chromedriver.exe' 
# -----------------------------

def run_app():
    """Starts the Flask app in a separate thread."""
    app = create_app()
    app.run(debug=False, use_reloader=False, host='localhost', port=5000)

# 1. Start the Flask app in the background
threading.Thread(target=run_app, daemon=True).start()
print("Waiting for Flask app to start (2 seconds)...")
time.sleep(2) # Give the server a second to start

# 2. Initialize the Selenium driver
print("Initializing Selenium Web Driver...")
# --- UPDATED: This is the new, correct way to start Chrome ---
driver = webdriver.Chrome(service=Service(DRIVER_PATH))

print("Driver initialized. Running test...")

try:
    # 3. Go to the website
    driver.get('http://localhost:5000/')
    print("ACTION: Went to home page.")
    time.sleep(1)

    # 4. Find the first event and click it
    # We must have an event in the DB for this to work
    # Please run the app and create one event as an admin first.
    first_event = driver.find_element("class name", "event-card")
    first_event.click()
    print("ACTION: Clicked on the first event.")
    time.sleep(1)

    # 5. We are on the details page. Fill out the form
    driver.find_element("id", "name").send_keys("Test Student Selenium")
    driver.find_element("id", "email").send_keys("selenium@test.com")
    print("ACTION: Filled out registration form.")
    time.sleep(1)

    # 6. Click the "Register" button
    driver.find_element("tag name", "button").click()
    print("ACTION: Clicked 'Register'.")
    time.sleep(1)

    # 7. Check if we are on the success page
    success_message = driver.find_element("tag name", "h1").text
    
    if "Registration Successful!" in success_message:
        print("---------------------------------")
        print("✅ TEST PASSED - Selenium test successful!")
        print("---------------------------------")
    else:
        print("---------------------------------")
        print("❌ TEST FAILED - 'Registration Successful!' message not found.")
        print("---------------------------------")

except Exception as e:
    print(f"❌ TEST FAILED with error: {e}")

finally:
    # 8. Close the browser
    driver.quit()
    print("Test finished. Browser closed.")