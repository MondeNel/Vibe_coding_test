from flask import request, jsonify, render_template, redirect, url_for

# In-memory user storage
users = {}
next_user_id = 1

def register_routes(app):
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

    # =========================
    # Frontend: Signup Page
    # =========================
    @app.route('/signup_page', methods=['GET', 'POST'])
    def signup_page():
        message = None
        if request.method == 'POST':
            name = request.form.get('name')
            surname = request.form.get('surname')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if not all([name, surname, email, password, confirm_password]):
                message = 'All fields are required.'
            elif password != confirm_password:
                message = 'Passwords do not match.'
            elif email in users:
                message = 'User already exists.'
            else:
                global next_user_id
                user = {
                    'id': next_user_id,
                    'name': name,
                    'surname': surname,
                    'password': password
                }
                users[email] = user
                next_user_id += 1
                return redirect(url_for('login_page'))
        return render_template('signup.html', message=message)

    # =========================
    # Frontend: Login Page
    # =========================
    @app.route('/login_page', methods=['GET', 'POST'])
    def login_page():
        message = None
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = users.get(email)
            if not email or not password:
                message = 'Email and password required.'
            elif not user or user['password'] != password:
                message = 'Invalid credentials.'
            else:
                return redirect(url_for('user_management'))
        return render_template('login.html', message=message)

    # =========================
    # Frontend: User Management Page
    # =========================
    @app.route('/users_page', methods=['GET', 'POST'])
    def user_management():
        message = None
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                name = request.form.get('name')
                surname = request.form.get('surname')
                email = request.form.get('email')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')
                if not all([name, surname, email, password, confirm_password]):
                    message = 'All fields are required.'
                elif password != confirm_password:
                    message = 'Passwords do not match.'
                elif email in users:
                    message = 'User already exists.'
                else:
                    global next_user_id
                    user = {
                        'id': next_user_id,
                        'name': name,
                        'surname': surname,
                        'password': password
                    }
                    users[email] = user
                    next_user_id += 1
                    message = 'User added successfully.'
            elif action == 'update':
                user_id_str = request.form.get('user_id')
                if user_id_str is None:
                    message = 'User ID is required for update.'
                else:
                    user_id = int(user_id_str)
                    name = request.form.get('name')
                    surname = request.form.get('surname')
                    password = request.form.get('password')
                    confirm_password = request.form.get('confirm_password')
                    for user in users.values():
                        if user['id'] == user_id:
                            if password:
                                if not confirm_password or password != confirm_password:
                                    message = 'Passwords do not match or missing confirm_password.'
                                    break
                                user['password'] = password
                            user['name'] = name or user['name']
                            user['surname'] = surname or user['surname']
                            message = 'User updated successfully.'
                            break
                    else:
                        message = 'User not found.'
            elif action == 'delete':
                user_id_str = request.form.get('user_id')
                if user_id_str is None:
                    message = 'User ID is required for delete.'
                else:
                    user_id = int(user_id_str)
                    for email, user in list(users.items()):
                        if user['id'] == user_id:
                            del users[email]
                            message = 'User deleted successfully.'
                            break
                    else:
                        message = 'User not found.'
        user_list = [
            {'id': user['id'], 'name': user['name'], 'surname': user['surname'], 'email': email}
            for email, user in users.items()
        ]
        return render_template('users.html', users=user_list, message=message) 