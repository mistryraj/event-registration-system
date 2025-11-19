import pytest
from app import create_app, db, Event, Registration

# This test will check SERS-5, SERS-6, and SERS-7
def test_full_registration_flow(client):
    """
    GIVEN a complete app and a test client
    WHEN an admin creates an event
    AND a student views that event's details
    AND the student registers for the event
    THEN check that the registration is saved to the database.
    """
    # 1. SETUP: Admin creates an event
    with client.application.app_context():
        test_event = Event(title='Test Event', description='Test Desc', event_date='2025-11-30')
        db.session.add(test_event)
        db.session.commit()
        # We need the ID for the URL, so we get it from the DB
        event_id = test_event.id

    # 2. (SERS-5): Student clicks the event on the dashboard
    # (We test this by going directly to the details page URL)
    response_details = client.get(f'/event/{event_id}')
    assert response_details.status_code == 200
    assert b"Register for this Event" in response_details.data

    # 3. (SERS-6): Student submits the registration form
    response_register = client.post(f'/register/{event_id}', data={
        'name': 'Raj Mistry',
        'email': 'raj@example.com'
    })
    
    # Should redirect to the success page
    assert response_register.status_code == 302
    assert response_register.location == '/register/success'

    # 4. Check the success page
    response_success = client.get('/register/success')
    assert response_success.status_code == 200
    assert b"Registration Successful!" in response_success.data

    # 5. FINAL CHECK: Was the registration saved to the database?
    with client.application.app_context():
        # Find the registration in the DB
        reg = Registration.query.first()
        assert reg is not None
        assert reg.student_name == 'Raj Mistry'
        assert reg.student_email == 'raj@example.com'
        assert reg.event_id == event_id