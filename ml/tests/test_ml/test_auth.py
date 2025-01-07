from django.test import TestCase
from ml.api.auth import ApiAuth
from django.conf import settings

class TestApiAuth(TestCase):
    def setUp(self):
        self.auth = ApiAuth()
        self.valid_token = settings.SHARED_SECRET_KEY

    def test_authenticate_valid(self):
        request = type('Request', (), {'headers': {'Authorization': f'Bearer {self.valid_token}'}})()
        result = self.auth.authenticate(request, self.valid_token)
        self.assertEqual(result, self.valid_token)

    def test_authenticate_invalid(self):
        invalid_token = "invalid_token"
        request = type('Request', (), {'headers': {'Authorization': f'Bearer {invalid_token}'}})()
        result = self.auth.authenticate(request, invalid_token)
        self.assertIsNone(result)

    def test_authenticate_no_token(self):
        request = type('Request', (), {'headers': {}})()
        with self.assertRaises(Exception) as context:
            self.auth.authenticate(request, None)
        self.assertEqual(str(context.exception), "No authentication token provided")

    def test_authenticate_with_exception(self):
        request = type('Request', (), {'headers': {'Authorization': None}})()
        result = self.auth.authenticate(request, "token")
        self.assertIsNone(result)

    def test_create_token(self):
        token = self.auth.create_token()
        self.assertTrue(token.startswith('Bearer '))
        self.assertIn(settings.SHARED_SECRET_KEY, token)

    def test_verify_token_valid(self):
        self.assertTrue(self.auth.verify_token(self.valid_token))

    def test_verify_token_invalid(self):
        self.assertFalse(self.auth.verify_token("invalid_token"))