# QA TestLab

## Overview
QA TestLab is a simple authentication system built with Django, designed to help QA engineers practice API testing in Postman. It provides basic authentication endpoints that allow users to sign up, log in, and access a protected dashboard. The system uses Django's built-in authentication framework to securely manage user credentials.

## Features
- User Sign-up with validation
- User Login with session handling
- Protected Dashboard (only accessible after login)
- Logout functionality

## Installation
### 1. Clone the Repository
```bash
git clone <repository_url>
cd qa-testlab
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv env
env\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional, for Admin Panel)
```bash
python manage.py createsuperuser
```

### 6. Start the Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Endpoints
| Endpoint      | Method | Description                  |
|--------------|--------|------------------------------|
| `/`          | GET    | Landing page                 |
| `/signup/`   | POST   | User registration            |
| `/login/`    | POST   | User authentication          |
| `/dashboard/`| GET    | Protected user dashboard     |
| `/logout/`   | GET    | Logs out the user            |

## Testing Authentication with Postman
1. **Sign Up:** Send a `POST` request to `/signup/` with `username`, `password`, and `confirm_password`.
2. **Login:** Send a `POST` request to `/login/` with `username` and `password`.
3. **Access Dashboard:** Send a `GET` request to `/dashboard/` (should be accessible only after login).
4. **Logout:** Send a `GET` request to `/logout/`.

## License
This project is open-source and available under the MIT License.

