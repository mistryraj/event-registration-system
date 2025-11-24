# Smart Event Registration System (SERS)

A Flask-based web application that allows the admin to create and manage events and enables students to view and register for the events.  
The project follows Agile Scrum methodology, Test-Driven Development (TDD), and Continuous Integration using GitHub Actions.

---

## Features

### Admin
- Admin can login through their credential
- Create new events
- View all student registrations
- Manage events

### Student
- View all upcoming events
- Read event details
- Register for events
- Receive confirmation email

### Testing
- Pytest-based unit tests
- Integration and route tests
- Selenium end-to-end browser tests

### CI
- GitHub Actions pipeline running:
  - Automated tests
  - Linting
  - Security checks
  - Build verification
- Head Selenium execution for CI compatibility

---

## Technology Stack

### Backend
- Flask
- SQLite database

### Frontend
- HTML and CSS
  
### Testing Frameworks
- Pytest
- Selenium WebDriver
- webdriver-manager
---

## Project Structure

```
Event-Registration-System/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline 
├── .pytest_cache/                    # Pytest execution cache
├── templates/                        # HTML templates 
├── app.py                            # Main Flask application entry point
├── chromedriver.exe                  # Selenium Chrome WebDriver (local testing)
├── conftest.py                       # Pytest fixtures and test configuration
├── events.db                         # SQLite database storing events and registrations
├── requirements.txt                  # All required Python packages
├── test_admin_login.py               # Test: Admin login authentication
├── test_admin_view_registration.py   # Test: Admin viewing student registrations
├── test_create_event.py              # Test: Event creation workflow
├── test_functional_selenium.py       # Selenium full end-to-end UI test
├── test_registration_flow.py         # Test: Student registration flow
└── test_student_dashboard.py         # Test: Student dashboard event listing
```

---

## Database Schema

### Event Table
- id
- title
- description
- date

### Registration Table
- id
- student_name
- student_email
- event_id (Foreign Key)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Display all events |
| GET | /event/<id> | Show event details |
| GET/POST | /register/<id> | Student registration |
| GET/POST | /admin/login | Admin login |
| GET | /admin/dashboard | Admin dashboard |
| GET | /admin/registrations | View registrations |
| GET/POST | /admin/create-event | Create event |

---

## How to Run the Application

### Step 1: Install dependencies
```
pip install -r requirements.txt
```

### Step 2: Start the application
```
python app.py
```

### Step 3: Open the browser
```
http://localhost:5000
```

---

## How to Run Tests

### Run all tests
```
pytest -v
```

### Run Selenium functional test
```
python -m test_functional_selenium.py
```

---

## CI Pipeline (GitHub Actions)

The pipeline includes:
- Python version matrix (3.9, 3.10, 3.11)
- Installing dependencies
- Running all Pytest suites
- Running head Selenium when required
- Linting with flake8 and pylint
- Security scanning with safety

All pipeline checks are currently passing.

---

