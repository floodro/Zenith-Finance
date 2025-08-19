# Zenith - A Personal Finance Management App

A personal finance tracking web application built with Django. This project allows users to manage their income and expenses, view financial summaries on a dashboard, and maintain their user profile.

## Features
-   **User Authentication**: Secure user registration, login, and logout functionality.
-   **Financial Dashboard**: An at-a-glance view of total balance, total income, and total expenses.
-   **Transaction Management**:
    -   List all personal transactions with details.
    -   Add new income or expense transactions through a dedicated form.
    -   Categorize transactions as 'Income' or 'Expense'.
-   **Profile Management**:
    -   View and edit user information (first name, last name, email).
    -   Fields are disabled by default and can be enabled with an "Edit" button for safe updates.

-   **Admin Interface**: A basic (work-in-progress) view for admins to upload transactions in bulk.

## Technology Stack

-   **Backend**: Python, Django
-   **Frontend**: HTML, CSS, JavaScript, Chart.js
-   **Database**: SQLite

## Setup and Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)

### 1. Clone the Repository

Clone this project to your local machine.
```bash
git clone <your-repository-url>
cd <repository-folder-name>
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

-   **For macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

-   **For Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
*(Note: If you don't have a `requirements.txt` file yet, you can create one by running `pip freeze > requirements.txt` after installing Django).*

### 4. Apply Database Migrations

Apply the database schema and create the necessary tables.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

A superuser is required to access the Django admin interface.
```bash
python manage.py createsuperuser
```
Follow the prompts to create a username and password.

### 6. Run the Development Server

Start the Django development server.
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Register a New Account**: Navigate to `http://127.0.0.1:8000/signup/` to create a new user account.
2.  **Log In**: Once registered, go to the login page (`http://127.0.0.1:8000/`) to access your account.
3.  **Dashboard**: After logging in, you will be redirected to your personal dashboard where you can see a summary of your finances.
4.  **Add a Transaction**: Go to the "Transactions" tab and click the "Add New Transaction" button to record a new income or expense.
5.  **Edit Your Profile**: Go to the "Profile" tab to view or update your personal information. Click the "Edit Profile" button to enable the fields.
6.  **Reports Page**: Go to the "Reports" tab to view data with charts and graphs to show spending trends and income vs. expense breakdowns.
7.   **Settings Page**: Implement functionality for users to change their password and manage notification preferences.
8.   **Accounts Management**: Add the ability to manage multiple financial accounts (e.g., checking, savings, credit card).
