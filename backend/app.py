from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage
users = {}
next_user_id = 1

@app.route('/signup', methods=['POST'])
def signup():
    global next_user_id
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not all([name, surname, email, password, confirm_password]):
        return jsonify({'error': 'All fields are required: name, surname, email, password, confirm_password'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    if email in users:
        return jsonify({'error': 'User already exists'}), 409
    user = {
        'id': next_user_id,
        'name': name,
        'surname': surname,
        'password': password
    }
    users[email] = user
    next_user_id += 1
    return jsonify({'message': 'User created successfully', 'id': user['id']}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if users.get(username) != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful'}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    for user in users.values():
        if user['id'] == user_id:
            user_data = {
                'id': user['id'],
                'name': user['name'],
                'surname': user['surname']
            }
            return jsonify(user_data), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_all_users():
    user_list = [
        {'id': user['id'], 'name': user['name'], 'surname': user['surname']}
        for user in users.values()
    ]
    return jsonify(user_list), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users.values():
        if user['id'] == user_id:
            name = data.get('name', user['name'])
            surname = data.get('surname', user['surname'])
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password:
                if not confirm_password or password != confirm_password:
                    return jsonify({'error': 'Passwords do not match or missing confirm_password'}), 400
                user['password'] = password
            user['name'] = name
            user['surname'] = surname
            return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for email, user in list(users.items()):
        if user['id'] == user_id:
            del users[email]
            return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 