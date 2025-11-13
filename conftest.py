import pytest
from app import create_app, db

@pytest.fixture
def client():
    # --- Create a temporary test database ---
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    # Use an "in-memory" SQLite database for tests. It's fast and disappears after.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # Create all database tables
            db.create_all()
        
        yield client # This is where the test runs
        
        # --- NEW CLEANUP CODE ---
        # After the test is done, drop all tables
        # to ensure a clean state for the next test.
        with app.app_context():
            db.session.remove()
            db.drop_all()