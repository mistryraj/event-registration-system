import pytest
from app import create_app, db, Event # Import db and Event

# TEST 1: Check that the "Create Event" page loads
def test_create_event_page_loads(client):
    response = client.get('/admin/event/create')
    assert response.status_code == 200
    assert b"<h1>Create New Event</h1>" in response.data

# TEST 2: Check that submitting the form works
def test_create_event_submission(client):
    response = client.post('/admin/event/create', data={
        'title': 'New Tech Talk',
        'description': 'A talk about Agile',
        'event_date': '2025-12-01'
    })
    
    # Check that it redirects
    assert response.status_code == 302
    assert response.location == '/admin/dashboard'
    
    # --- NEW TEST: Check that the data was saved to the DB ---
    # We query the database to see if the event is there.
    event_from_db = Event.query.first()
    assert event_from_db is not None
    assert event_from_db.title == 'New Tech Talk'