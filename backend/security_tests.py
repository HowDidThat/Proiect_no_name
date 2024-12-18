import unittest
import requests
import jwt
from datetime import datetime, timedelta
import json
import re


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/api"
        self.test_user = {
            "username": "securitytester",
            "password": "SecurePass123!",
            "email": "security@test.com",
            "institution": "Test Hospital",
            "year_of_study": 3
        }

        try:
            self.register_user()
        except:
            pass

    def register_user(self):
        return requests.post(
            f"{self.base_url}/auth/register",
            json=self.test_user
        )

    def login_user(self):
        return requests.post(
            f"{self.base_url}/auth/login",
            json={
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
        )

    def test_password_complexity(self):
        weak_passwords = [
            "short",
            "onlylowercase",
            "ONLYUPPERCASE",
            "12345678",
            "pass word",
            "common_password"
        ]

        for password in weak_passwords:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    **self.test_user,
                    "username": f"test_user_{password}",
                    "password": password
                }
            )
            self.assertEqual(response.status_code, 400)

    def test_sql_injection_prevention(self):
        injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "admin'--",
            "' OR id IS NOT NULL; --"
        ]

        for payload in injection_payloads:
            login_response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": payload,
                    "password": payload
                }
            )
            self.assertEqual(login_response.status_code, 401)

            register_response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "username": payload,
                    "password": "ValidPass123!",
                    "email": "test@test.com",
                    "institution": "Test Hospital",
                    "year_of_study": 3
                }
            )
            self.assertEqual(register_response.status_code, 400)


    def test_brute_force_prevention(self):
        for _ in range(10):
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": "nonexistent",
                    "password": "wrongpass"
                }
            )

        self.assertEqual(response.status_code, 401)

    def test_token_security(self):
        login_response = self.login_user()
        self.assertEqual(login_response.status_code, 200)

        valid_token = login_response.cookies.get('access_token')

        expired_payload = {
            'user_id': 1,
            'exp': datetime.utcnow() - timedelta(hours=1),
            'iat': datetime.utcnow() - timedelta(hours=2),
            'type': 'access'
        }
        expired_token = jwt.encode(
            expired_payload,
            'any_key',
            algorithm='HS256'
        )

        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        self.assertEqual(response.status_code, 401)

        tampered_token = valid_token + "tampered"
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {tampered_token}"}
        )
        self.assertEqual(response.status_code, 401)

    def test_xss_prevention(self):
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src='x' onerror='alert(1)'>",
            "<svg onload='alert(1)'>",
            "'-alert(1)-'"
        ]

        for payload in xss_payloads:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    **self.test_user,
                    "username": f"test_user_{len(payload)}",
                    "institution": payload
                }
            )
            self.assertEqual(response.status_code, 400)

    def test_secure_headers(self):
        response = requests.get(f"{self.base_url}/auth/me")
        headers = response.headers

        self.assertIn('X-Content-Type-Options', headers)
        self.assertIn('X-Frame-Options', headers)


if __name__ == '__main__':
    unittest.main()