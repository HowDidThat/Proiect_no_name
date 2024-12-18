# tests.py
import os
import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter("ignore", CacheKeyWarning)

from django.test import TestCase
from ninja.testing import TestClient

from django.conf import settings
from .models import User
from .views import auth_router, create_tokens

os.environ.setdefault('SECRET_KEY', 'pisica')
os.environ.setdefault('SHARED_SECRET_KEY', 'pinguin')


class AuthenticationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        settings.SECRET_KEY = os.getenv('SECRET_KEY')
        settings.SHARED_SECRET_KEY = os.getenv('SHARED_SECRET_KEY')

    def setUp(self):
        self.client = TestClient(auth_router)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            institution='Test Hospital',
            year_of_study=3
        )

        self.access_token, self.refresh_token = create_tokens(self.user.id)
        self.user_headers = {"Authorization": f"Bearer {self.access_token}"}

        self.register_url = '/register'
        self.login_url = '/login'
        self.logout_url = '/logout'
        self.me_url = '/me'
        self.refresh_url = '/refresh'

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'ValidPass123!',
                'institution': 'New Hospital',
                'year_of_study': 2
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Registration successful")
        self.assertTrue('access_token' in response.cookies)
        self.assertTrue('refresh_token' in response.cookies)

    def test_duplicate_username_registration(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'testuser',
                'email': 'another@example.com',
                'password': 'ValidPassword123!',
                'institution': 'Hospital',
                'year_of_study': 1
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'username' and 'exists' in error['message'] for error in errors))

    def test_protected_endpoint_accepts_valid_auth(self):
        response = self.client.get(
            self.me_url,
            headers=self.user_headers
        )
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data['username'], 'testuser')
        self.assertEqual(user_data['email'], 'test@example.com')

    def test_refresh_token(self):
        response = self.client.post(
            self.refresh_url,
            headers={"Authorization": f"Bearer {self.refresh_token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Tokens refreshed")
        self.assertTrue('access_token' in response.cookies)
        self.assertTrue('refresh_token' in response.cookies)

    def test_registration_invalid_username(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'u@',
                'email': 'test@example.com',
                'password': 'ValidPass123!',
                'institution': 'Test Hospital',
                'year_of_study': 3
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'username' for error in errors))

    def test_registration_invalid_email(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'validuser',
                'email': 'not-an-email',
                'password': 'ValidPass123!',
                'institution': 'Test Hospital',
                'year_of_study': 3
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'email' for error in errors))

    def test_registration_weak_password(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'validuser',
                'email': 'test@example.com',
                'password': '123',
                'institution': 'Test Hospital',
                'year_of_study': 3
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'password' for error in errors))

    def test_registration_invalid_year(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'validuser',
                'email': 'test@example.com',
                'password': 'ValidPass123!',
                'institution': 'Test Hospital',
                'year_of_study': 8
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'year_of_study' for error in errors))

    def test_registration_invalid_institution(self):
        response = self.client.post(
            self.register_url,
            json={
                'username': 'validuser',
                'email': 'test@example.com',
                'password': 'ValidPass123!',
                'institution': '  ',
                'year_of_study': 3
            }
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()['errors']
        self.assertTrue(any(error['field'] == 'institution' for error in errors))

    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'testpass123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Login successful")
        self.assertTrue('access_token' in response.cookies)
        self.assertTrue('refresh_token' in response.cookies)

    def test_user_cannot_login_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'wrongpass'
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['message'], "Invalid credentials")

    def test_protected_endpoint_requires_auth(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_accepts_valid_auth(self):
        login_response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'testpass123'
            }
        )

        access_token = login_response.cookies['access_token'].value

        response = self.client.get(
            self.me_url,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data['username'], 'testuser')
        self.assertEqual(user_data['email'], 'test@example.com')

    def test_refresh_token(self):
        login_response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'testpass123'
            }
        )

        refresh_token = login_response.cookies['refresh_token'].value

        refresh_response = self.client.post(
            self.refresh_url,
            headers={'Authorization': f'Bearer {refresh_token}'}
        )

        self.assertEqual(refresh_response.status_code, 200)
        self.assertEqual(refresh_response.json()['message'], "Tokens refreshed")
        self.assertTrue('access_token' in refresh_response.cookies)
        self.assertTrue('refresh_token' in refresh_response.cookies)

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Logout successful")

        self.assertTrue(
            response.cookies['access_token'].get('max-age') == 0 or
            response.cookies['access_token'].value == ''
        )
        self.assertTrue(
            response.cookies['refresh_token'].get('max-age') == 0 or
            response.cookies['refresh_token'].value == ''
        )
