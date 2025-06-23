import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# =========================
# Test Register User
# =========================
def test_signup_success(client):
    response = client.post('/signup', json={
        'name': 'Test',
        'surname': 'User',
        'email': 'testuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_signup_missing_fields(client):
    response = client.post('/signup', json={
        'name': 'Test',
        'surname': 'User',
        'email': 'testuser2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400


def test_signup_password_mismatch(client):
    response = client.post('/signup', json={
        'name': 'Test',
        'surname': 'User',
        'email': 'testuser3@example.com',
        'password': 'password123',
        'confirm_password': 'wrongpass'
    })
    assert response.status_code == 400


def test_signup_duplicate_email(client):
    client.post('/signup', json={
        'name': 'Test',
        'surname': 'User',
        'email': 'testuser4@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.post('/signup', json={
        'name': 'Test',
        'surname': 'User',
        'email': 'testuser4@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 409

# =========================
# Test Login User
# =========================
def test_login_success(client):
    client.post('/signup', json={
        'name': 'Login',
        'surname': 'User',
        'email': 'loginuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.post('/login', json={
        'email': 'loginuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'


def test_login_invalid_credentials(client):
    response = client.post('/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

# =========================
# Test Get User by ID
# =========================
def test_get_user_by_id(client):
    signup_resp = client.post('/signup', json={
        'name': 'Get',
        'surname': 'User',
        'email': 'getuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    user_id = signup_resp.get_json()['id']
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Get'
    assert data['surname'] == 'User'


def test_get_user_by_id_not_found(client):
    response = client.get('/user/9999')
    assert response.status_code == 404

# =========================
# Test Get All Users
# =========================
def test_get_all_users(client):
    client.post('/signup', json={
        'name': 'All',
        'surname': 'User',
        'email': 'alluser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# =========================
# Test Update User
# =========================
def test_update_user(client):
    signup_resp = client.post('/signup', json={
        'name': 'Update',
        'surname': 'User',
        'email': 'updateuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    user_id = signup_resp.get_json()['id']
    response = client.put(f'/user/{user_id}', json={
        'name': 'Updated',
        'surname': 'User',
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User updated successfully'


def test_update_user_not_found(client):
    response = client.put('/user/9999', json={
        'name': 'No',
        'surname': 'User'
    })
    assert response.status_code == 404

# =========================
# Test Delete User
# =========================
def test_delete_user(client):
    signup_resp = client.post('/signup', json={
        'name': 'Delete',
        'surname': 'User',
        'email': 'deleteuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    user_id = signup_resp.get_json()['id']
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User deleted successfully'


def test_delete_user_not_found(client):
    response = client.delete('/user/9999')
    assert response.status_code == 404 