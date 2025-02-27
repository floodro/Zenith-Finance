from django.test import TestCase, Client
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_signup(self):
        response = self.client.post('/signup/', {
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success

    def test_signup_password_mismatch(self):
        response = self.client.post('/signup/', {
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on signup page
        self.assertContains(response, 'Passwords do not match!')

    def test_login_success(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to dashboard

    def test_login_invalid_credentials(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password!')

    def test_dashboard_access_without_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_dashboard_access_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)  # Should be accessible

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Redirects to login page
