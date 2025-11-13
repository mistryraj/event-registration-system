import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # We use "test_client" to simulate a logged-in user
    with app.test_client() as client:
        # We simulate the login first
        with client.session_transaction() as sess:
            # (In a real app, we'd log in, but for testing,
            # we can just set the session variable)
            # Let's assume our app will set 'admin_logged_in' = True
            pass
        yield client

# TEST 1: Check that the "Create Event" page loads
def test_create_event_page_loads(client):
    """
    GIVEN a logged-in admin
    WHEN the '/admin/event/create' page is requested (GET)
    THEN check that the response contains the creation form.
    """
    response = client.get('/admin/event/create')
    assert response.status_code == 200
    assert b"<h1>Create New Event</h1>" in response.data

# TEST 2: Check that submitting the form works
def test_create_event_submission(client):
    """
    GIVEN a logged-in admin
    WHEN the '/admin/event/create' page is submitted (POST)
    THEN check that the event is "created" and redirects to the dashboard.
    """
    response = client.post('/admin/event/create', data={
        'title': 'New Tech Talk',
        'description': 'A talk about Agile',
        'event_date': '2025-12-01'
    })
    
    # It should redirect back to the dashboard
    assert response.status_code == 302
    assert response.location == '/admin/dashboard'