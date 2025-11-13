import pytest
from app import create_app

# TEST 1: Test that the admin login page loads (GET request)
def test_admin_login_page_loads(client):
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b"<h2>Admin Login</h2>" in response.data

# TEST 2: Test a FAILED login (POST request)
def test_failed_admin_login(client):
    response = client.post('/admin/login', data={
        'username': 'admin',
        'password': 'wrong_password'
    })
    assert b"Invalid username or password" in response.data

# TEST 3: Test a SUCCESSFUL login (POST request)
def test_successful_admin_login(client):
    response = client.post('/admin/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    assert response.status_code == 302
    assert response.location == '/admin/dashboard'