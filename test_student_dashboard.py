import pytest
from app import create_app, db, Event # Import db and Event

# TEST 1: Test that the student page loads when NO events exist
def test_student_dashboard_empty(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"No events are scheduled" in response.data

# TEST 2: Test that the student page shows events
def test_student_dashboard_with_events(client):
    # --- First, manually add an event to our test database ---
    with client.application.app_context():
        test_event = Event(
            title='My Test Event',
            description='This is the description.',
            event_date='2025-11-20'
        )
        db.session.add(test_event)
        db.session.commit()
    # --------------------------------------------------------
    
    # Now, we visit the student page
    response = client.get('/')
    
    # Check that the event's details are on the page
    assert response.status_code == 200
    assert b"My Test Event" in response.data
    assert b"This is the description." in response.data
    assert b"No events are scheduled" not in response.data