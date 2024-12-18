import random
import string

from locust import HttpUser, task, between


class QuizAppUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def generate_unique_username(self):
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"loadtester_{random_suffix}"

    def on_start(self):
        self.username = self.generate_unique_username()
        self.password = "TestPass123!"

        register_response = self.client.post("/api/auth/register",
                                             json={
                                                 "username": self.username,
                                                 "password": self.password,
                                                 "email": f"{self.username}@test.com",
                                                 "institution": "Test Hospital",
                                                 "year_of_study": 3
                                             },
                                             catch_response=True
                                             )

        login_response = self.client.post("/api/auth/login",
                                          json={
                                              "username": self.username,
                                              "password": self.password
                                          }
                                          )

        if login_response.cookies:
            self.access_token = login_response.cookies.get('access_token')
            self.refresh_token = login_response.cookies.get('refresh_token')
        else:
            data = login_response.json()
            self.access_token = data.get('access_token')
            self.refresh_token = data.get('refresh_token')

        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    @task(2)
    def get_quizzes(self):
        with self.client.get(
                "/api/quiz/",
                headers=self.headers,
                catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def create_quiz(self):
        with self.client.post(
                "/api/quiz/",
                json={
                    "title": f"Load Test Quiz - {self.username}",
                    "description": "Quiz created during load testing",
                    "quiz_type": "disease_to_symptoms",
                    "difficulty": "medium"
                },
                headers=self.headers,
                catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def refresh_token(self):
        with self.client.post(
                "/api/auth/refresh",
                headers={"Authorization": f"Bearer {self.refresh_token}"},
                catch_response=True
        ) as response:
            if response.status_code == 200:
                if response.cookies:
                    self.access_token = response.cookies.get('access_token')
                    self.refresh_token = response.cookies.get('refresh_token')
                    self.headers = {"Authorization": f"Bearer {self.access_token}"}
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
