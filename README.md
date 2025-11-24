# Smart Event Registration System (SERS)

A Flask-based web application that allows administrators to create and manage events and enables students to view and register for them.  
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
- Receive registration confirmation (console log)

### Testing
- Pytest-based unit tests
- Integration and route tests
- Selenium end-to-end browser tests
- More than 95 percent code coverage

### CI
- GitHub Actions pipeline running:
  - Automated tests
  - Linting
  - Security checks
  - Build verification
- Headless Selenium execution for CI compatibility

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

### Run all tests with coverage
```
pytest -v --cov=app --cov-report=html
```

### Run Selenium functional test
```
pytest tests/test_functional_selenium.py
```

---

## CI/CD Pipeline (GitHub Actions)

The pipeline includes:
- Python version matrix (3.9, 3.10, 3.11)
- Installing dependencies
- Running all Pytest suites
- Running head Selenium when required
- Linting with flake8 and pylint
- Security scanning with safety

All pipeline checks are currently passing.

---

## SOLID Principles Applied

- Single Responsibility: Routes and models are strictly separated in scope.
- Open/Closed: New features were added in Sprint 2 without modifying Sprint 1 logic.
- Liskov Substitution: SQLAlchemy models work uniformly with db.session operations.
- Interface Segregation: Models contain only necessary fields and logic.
- Dependency Inversion: Database operations rely on SQLAlchemy abstractions.

---

## Agile Metrics

- Story Points Completed: 35
- Two sprints executed
  - Sprint 1: 12 story points
  - Sprint 2: 23 story points
- Average Velocity: 17.5 SP per sprint
- Test Coverage: 95 percent or more
- Build Success Rate: 100 percent

---

## Technical Challenges and Solutions

1. Test interference and database locking  
   Solution: In-memory SQLite database and isolated fixtures using conftest.py.

2. Selenium failures in CI (headless execution issues)  
   Solution: Automatic environment detection and forced headless mode inside CI.

3. Chrome driver version mismatches  
   Solution: webdriver-manager integration to auto-download correct drivers.

4. Deprecation warnings for datetime.utcnow()  
   Solution: Replaced with timezone-aware datetime.now(timezone.utc).


