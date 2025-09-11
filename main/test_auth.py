# test_auth.py - Fixed version with Django setup
import os
import sys
import django
from django.conf import settings

# Configure Django settings BEFORE importing any Django modules
if not settings.configured:
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)
    
    # Set the settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    
    # Initialize Django
    django.setup()

# NOW we can safely import Django modules
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from main.forms import EnhancedUserCreationForm

# Test cases for authentication views in Django

@pytest.mark.django_db
def test_signup_view_success(client): 
    """
    Tests that a new user can be created successfully with strong password.
    """
    user_data = {
        'username': 'testuser123',
        'password1': 'StrongPassword123!',  # Updated for Django form standard
        'password2': 'StrongPassword123!'   # Updated for Django form standard
    }
    
    assert User.objects.count() == 0
    
    signup_url = reverse('signup')
    response = client.post(signup_url, user_data)
    
    assert User.objects.count() == 1
    assert User.objects.filter(username='testuser123').exists()
    
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_signup_view_weak_password_rejected(client):
    """
    Tests that weak passwords are rejected during signup.
    """
    weak_user_data = {
        'username': 'weakuser',
        'password1': 'weak123',  # Missing uppercase, symbol
        'password2': 'weak123'
    }
    
    assert User.objects.count() == 0
    
    signup_url = reverse('signup')
    response = client.post(signup_url, weak_user_data)
    
    # User should not be created
    assert User.objects.count() == 0
    assert not User.objects.filter(username='weakuser').exists()
    
    # Should stay on signup page (not redirect)
    assert response.status_code == 200
    
    # Should contain password strength error messages
    response_content = response.content.decode()
    assert 'Password must contain at least one uppercase letter' in response_content


@pytest.mark.django_db
def test_signup_view_password_mismatch(client):
    """
    Tests that mismatched passwords are rejected.
    """
    mismatch_data = {
        'username': 'mismatchuser',
        'password1': 'StrongPassword123!',
        'password2': 'DifferentPassword456!'
    }
    
    signup_url = reverse('signup')
    response = client.post(signup_url, mismatch_data)
    
    # DEBUG: Print the actual content to see the real error message
    print("\n" + "="*50)
    print("RESPONSE CONTENT:")
    print(response.content.decode())
    print("="*50)
    
    # This will probably fail, but we'll see the actual content
    assert "password fields didn't match" in response.content.decode()

@pytest.mark.django_db
def test_signup_view_duplicate_username(client):
    """
    Tests that duplicate usernames are rejected.
    """
    # Create existing user first
    User.objects.create_user(username='existinguser', password='ExistingPass123!')
    
    duplicate_data = {
        'username': 'existinguser',  # Same username
        'password1': 'NewStrongPass123!',
        'password2': 'NewStrongPass123!'
    }
    
    assert User.objects.count() == 1  # One existing user
    
    signup_url = reverse('signup')
    response = client.post(signup_url, duplicate_data)
    
    # Should still only have one user
    assert User.objects.count() == 1
    
    # Should stay on signup page
    assert response.status_code == 200
    
    # Should contain username exists error
    response_content = response.content.decode()
    assert 'username already exists' in response_content


@pytest.mark.django_db
def test_password_strength_form_validation():
    """
    Tests the enhanced form validation directly.
    """
    # Test valid strong password
    valid_data = {
        'username': 'validuser',
        'password1': 'MyStr0ng!Password123',
        'password2': 'MyStr0ng!Password123'
    }
    form = EnhancedUserCreationForm(data=valid_data)
    assert form.is_valid()
    
    # Test weak password (missing requirements)
    weak_data = {
        'username': 'weakuser',
        'password1': 'weak',  # Too short, no uppercase, no symbol
        'password2': 'weak'
    }
    form = EnhancedUserCreationForm(data=weak_data)
    assert not form.is_valid()
    assert 'password1' in form.errors
    
    # Verify specific error messages
    password_errors = form.errors['password1']
    error_text = ' '.join(password_errors)
    assert 'at least 8 characters' in error_text
    assert 'uppercase letter' in error_text
    assert 'symbol' in error_text


@pytest.mark.django_db
def test_password_requirements_individually():
    """
    Tests each password requirement individually.
    """
    base_data = {'username': 'testuser'}
    
    # Test missing uppercase
    no_upper_data = base_data.copy()
    no_upper_data.update({
        'password1': 'lowercase123!',
        'password2': 'lowercase123!'
    })
    form = EnhancedUserCreationForm(data=no_upper_data)
    assert not form.is_valid()
    assert any('uppercase letter' in str(error) for error in form.errors['password1'])
    
    # Test missing number
    no_number_data = base_data.copy()
    no_number_data.update({
        'password1': 'NoNumbers!',
        'password2': 'NoNumbers!'
    })
    form = EnhancedUserCreationForm(data=no_number_data)
    assert not form.is_valid()
    assert any('number' in str(error) for error in form.errors['password1'])
    
    # Test missing symbol
    no_symbol_data = base_data.copy()
    no_symbol_data.update({
        'password1': 'NoSymbols123',
        'password2': 'NoSymbols123'
    })
    form = EnhancedUserCreationForm(data=no_symbol_data)
    assert not form.is_valid()
    assert any('symbol' in str(error) for error in form.errors['password1'])


@pytest.mark.django_db
def test_login_view(client): 
    """
    Tests that a registered user can log in successfully.
    """
    test_password = 'StrongPassword123!'  # Updated to meet new requirements
    user = User.objects.create_user(username='loginuser', password=test_password)
    
    login_url = reverse('login')
    response = client.post(login_url, {'username': 'loginuser', 'password': test_password})
    
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    
    assert '_auth_user_id' in client.session
    assert client.session['_auth_user_id'] == str(user.id)


@pytest.mark.django_db
def test_logout_view(client): 
    """
    Tests that a logged-in user can log out successfully.
    """
    test_password = 'StrongPassword123!'  # Updated to meet new requirements
    user = User.objects.create_user(username='logoutuser', password=test_password)
    
    client.login(username='logoutuser', password=test_password)
    
    assert '_auth_user_id' in client.session
    
    logout_url = reverse('logout')
    response = client.get(logout_url)
    
    assert response.status_code == 302
    assert response.url == reverse('login')
    
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_authenticated_user_redirected_from_signup(client):
    """
    Tests that authenticated users are redirected from signup page.
    """
    # Create and login user
    test_password = 'TestPassword123!'
    user = User.objects.create_user(username='testuser', password=test_password)
    client.force_login(user)
    
    signup_url = reverse('signup')
    response = client.get(signup_url)
    
    # Should redirect to dashboard
    assert response.status_code == 302
    assert response.url == reverse('dashboard')


# Pytest fixtures for reusable test data
@pytest.fixture
def strong_password_data():
    """Fixture for valid strong password data."""
    return {
        'username': 'stronguser',
        'password1': 'MyStr0ng!Password123',
        'password2': 'MyStr0ng!Password123'
    }


@pytest.fixture
def weak_password_data():
    """Fixture for weak password data."""
    return {
        'username': 'weakuser',
        'password1': 'weak123',
        'password2': 'weak123'
    }


@pytest.fixture
def existing_user():
    """Fixture for creating an existing user."""
    return User.objects.create_user(
        username='existinguser', 
        password='ExistingPass123!'
    )


@pytest.mark.django_db
def test_signup_with_fixtures(client, strong_password_data):
    """
    Test using fixtures for cleaner test data management.
    """
    assert User.objects.count() == 0
    
    response = client.post(reverse('signup'), strong_password_data)
    
    assert User.objects.count() == 1
    assert User.objects.filter(username=strong_password_data['username']).exists()
    assert response.status_code == 302


@pytest.mark.django_db 
def test_common_weak_passwords_rejected(client):
    """
    Tests that common weak passwords are rejected.
    """
    common_weak_passwords = [
        ('password123', 'password123'),
        ('12345678', '12345678'),  
        ('qwertyui', 'qwertyui'),
    ]
    
    for password1, password2 in common_weak_passwords:
        weak_data = {
            'username': f'user_{password1}',
            'password1': password1,
            'password2': password2
        }
        
        response = client.post(reverse('signup'), weak_data)
        
        # Should not create user
        assert not User.objects.filter(username=weak_data['username']).exists()
        # Should stay on signup page
        assert response.status_code == 200
        
        # Clean up for next iteration
        User.objects.filter(username=weak_data['username']).delete()