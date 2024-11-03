from django.test import TestCase
from ninja.testing import TestClient
from .models import User
from .views import auth_router


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = TestClient(auth_router)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            institution='Test Hospital',
            year_of_study=3
        )
        self.login_url = '/login'
        self.me_url = '/me'

    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'testpass123'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_user_cannot_login_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'wrongpass'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_requires_token(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_accepts_valid_token(self):
        login_response = self.client.post(
            self.login_url,
            json={
                'username': 'testuser',
                'password': 'testpass123'
            }
        )
        token = login_response.json()['token']

        response = self.client.get(
            self.me_url,
            headers={'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data['username'], 'testuser')
        self.assertEqual(user_data['email'], 'test@example.com')
