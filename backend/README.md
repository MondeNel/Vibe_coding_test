# Flask API Example Usage

## Signup
```
curl -X POST http://127.0.0.1:5000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "password": "testpass",
    "confirm_password": "testpass"
  }'
```

## Login
```
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@example.com", "password": "testpass"}'
```

## Get User by ID
```
curl http://127.0.0.1:5000/user/1
```

## Get All Users
```
curl http://127.0.0.1:5000/users
```

## Update User by ID
```
curl -X PUT http://127.0.0.1:5000/user/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane",
    "surname": "Smith",
    "password": "newpass",
    "confirm_password": "newpass"
  }'
```

## Delete User by ID
```
curl -X DELETE http://127.0.0.1:5000/user/1
```

Replace `1` with the desired user id and adjust the fields as needed. 