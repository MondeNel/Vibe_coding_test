from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage
users = {}
next_user_id = 1

# =========================
# Register User
# =========================
@app.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user with name, surname, email, password, and confirm_password.
    Returns user id on success.
    """
    global next_user_id
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    # Validate all fields are present
    if not all([name, surname, email, password, confirm_password]):
        return jsonify({'error': 'All fields are required: name, surname, email, password, confirm_password'}), 400
    # Check if passwords match
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    # Check if user already exists
    if email in users:
        return jsonify({'error': 'User already exists'}), 409
    # Create user and increment id
    user = {
        'id': next_user_id,
        'name': name,
        'surname': surname,
        'password': password
    }
    users[email] = user
    next_user_id += 1
    return jsonify({'message': 'User created successfully', 'id': user['id']}), 201

# =========================
# Login User
# =========================
@app.route('/login', methods=['POST'])
def login():
    """
    Login a user with email and password.
    Returns success message if credentials are valid.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Validate fields
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    user = users.get(email)
    # Check credentials
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful'}), 200

# =========================
# Get User by ID
# =========================
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Retrieve a user's details by their id (excluding password).
    """
    for user in users.values():
        if user['id'] == user_id:
            user_data = {
                'id': user['id'],
                'name': user['name'],
                'surname': user['surname']
            }
            return jsonify(user_data), 200
    return jsonify({'error': 'User not found'}), 404

# =========================
# Get All Users
# =========================
@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Retrieve a list of all users (excluding passwords).
    """
    user_list = [
        {'id': user['id'], 'name': user['name'], 'surname': user['surname']}
        for user in users.values()
    ]
    return jsonify(user_list), 200

# =========================
# Update User
# =========================
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user's name, surname, and/or password by their id.
    Password change requires confirm_password.
    """
    data = request.get_json()
    for user in users.values():
        if user['id'] == user_id:
            # Update name and surname if provided
            name = data.get('name', user['name'])
            surname = data.get('surname', user['surname'])
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            # If password is being changed, check confirmation
            if password:
                if not confirm_password or password != confirm_password:
                    return jsonify({'error': 'Passwords do not match or missing confirm_password'}), 400
                user['password'] = password
            user['name'] = name
            user['surname'] = surname
            return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

# =========================
# Delete User
# =========================
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by their id.
    """
    for email, user in list(users.items()):
        if user['id'] == user_id:
            del users[email]
            return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 