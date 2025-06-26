# Vibe Coding Test: User Management App

## Overview
A simple full-stack user management application built with Flask (backend) and HTML/CSS (frontend). Features include user registration, login, user management, and a RESTful API.

---

## Directory Structure
```
Vibe_coding_test/
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── requirements.txt
│   ├── test_routes.py
│   └── ...
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── users.html
│   └── static/
│       └── style.css
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MondeNel/Vibe_coding_test.git

cd Vibe_coding_test
```

### 2. Backend Setup
```bash
cd backend

python -m venv venv


# On Windows: source venv/bin/activate  

pip install -r requirements.txt
```

### 3. Run the App
```bash
python app.py
```
- The server will start at `http://127.0.0.1:5000/`

### 4. Frontend Usage
- The backend serves the frontend pages:
    - `http://127.0.0.1:5000/signup_page` — Signup page

    - `http://127.0.0.1:5000/login_page` — Login page

    - `http://127.0.0.1:5000/users_page` — User management (after login)

---

## API Endpoints

### Signup
```bash
POST http://127.0.0.1:5000/signup 

  '{
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "password": "testpass",
    "confirm_password": "testpass"
  }'
```

### Login
```bash
POST http://127.0.0.1:5000/login 
'{"email": "john.doe@example.com", "password": "testpass"}'
```

### Get User by ID
```bash
curl http://127.0.0.1:5000/user/1
```

### Get All Users
```bash
curl http://127.0.0.1:5000/users
```

### Update User by ID
```bash
PUT http://127.0.0.1:5000/user/1 '{
    "name": "Jane",
    "surname": "Smith",
    "password": "newpass",
    "confirm_password": "newpass"
  }'
```

### Delete User by ID
```bash
 DELETE http://127.0.0.1:5000/user/1
```

---

## Running Tests

From the `backend` directory:
```bash
pytest test_routes.py
```

---

## Notes
- All user data is stored in memory (no database).
- Passwords are stored in plain text (for demo only; do not use in production).
- The app is mobile responsive and works on all device sizes.
- For improvements, see the suggestions section in the codebase or ask for more features!
