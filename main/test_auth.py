import pytest
from django.contrib.auth.models import User
from django.urls import reverse

# Test cases for authentication views in Django
@pytest.mark.django_db
def test_signup_view(client): 
    """
    Tests that a new user can be created successfully.
    """

    user_data = {
        'username': 'testuser123',
        'password': 'StrongPassword123',
        'confirm_password': 'StrongPassword123'
    }
    
    assert User.objects.count() == 0
    
    signup_url = reverse('signup')
    response = client.post(signup_url, user_data)
    
    assert User.objects.count() == 1
    assert User.objects.filter(username='testuser123').exists()
    
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_login_view(client): 
    """
    Tests that a registered user can log in successfully.
    """
    test_password = 'StrongPassword123'
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
    test_password = 'StrongPassword123'
    user = User.objects.create_user(username='logoutuser', password=test_password)
    
    client.login(username='logoutuser', password=test_password)
    
    assert '_auth_user_id' in client.session
    
    logout_url = reverse('logout')
    response = client.get(logout_url)
    
    assert response.status_code == 302
    assert response.url == reverse('login')
    
    assert '_auth_user_id' not in client.session