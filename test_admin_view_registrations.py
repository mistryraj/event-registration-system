import pytest
from app import create_app, db, Event, Registration

def test_admin_view_registrations(client):
    """
    GIVEN a student has registered for an event
    WHEN the admin visits the '/admin/registrations' page
    THEN check that the student's registration info is displayed.
    """
    # 1. SETUP: Create an event and a registration
    with client.application.app_context():
        test_event = Event(title='Event for Admin', description='Test Desc', event_date='2025-12-10')
        db.session.add(test_event)
        db.session.commit()
        
        test_reg = Registration(
            student_name='Bhuvan Rathod',
            student_email='bhuvan@example.com',
            event_id=test_event.id
        )
        db.session.add(test_reg)
        db.session.commit()

    # 2. ACTION: Admin logs in and visits the page
    client.post('/admin/login', data={'username': 'admin', 'password': 'password123'})
    response = client.get('/admin/registrations')
    
    # 3. ASSERT: Check if the live data is on the page
    assert response.status_code == 200
    assert b"Bhuvan Rathod" in response.data       # Student name
    assert b"bhuvan@example.com" in response.data  # Student email
    assert b"Event for Admin" in response.data     # Event title