# quiz/tests.py
from django.test import TestCase
from ninja.testing import TestClient
from authentication.models import User
from authentication.views import create_token
from .views import quiz_router


class QuizTest(TestCase):
    def setUp(self):
        self.client = TestClient(quiz_router)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            institution='Test Hospital',
            year_of_study=3
        )
        # Create token
        self.token = create_token(self.user.id)
        self.quiz_url = ''
        self.submit_url = ''
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_can_create_quiz(self):
        response = self.client.post(
            self.quiz_url,
            json={
                'title': 'Test Quiz',
                'description': 'Test Description',
                'quiz_type': 'disease_to_symptoms',
                'difficulty': 'easy'
            },
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Test Quiz')

    def test_can_submit_quiz_answers(self):
        quiz_response = self.client.post(
            self.quiz_url,
            json={
                'title': 'Test Quiz',
                'description': 'Test Description',
                'quiz_type': 'disease_to_symptoms',
                'difficulty': 'easy'
            },
            headers=self.headers
        )
        quiz_id = quiz_response.json()['id']

        submit_response = self.client.post(
            f'{self.submit_url}/{quiz_id}',
            json={
                'answers': {
                    'question1': 'answer1',
                    'question2': 'answer2'
                }
            },
            headers=self.headers
        )

        self.assertEqual(submit_response.status_code, 200)
        self.assertIn('score', submit_response.json())

    def test_cannot_submit_quiz_without_answers(self):
        quiz_response = self.client.post(
            self.quiz_url,
            json={
                'title': 'Test Quiz',
                'description': 'Test Description',
                'quiz_type': 'disease_to_symptoms',
                'difficulty': 'easy'
            },
            headers=self.headers
        )
        quiz_id = quiz_response.json()['id']

        submit_response = self.client.post(
            f'{self.submit_url}/{quiz_id}',
            json={
                'answers': {}
            },
            headers=self.headers
        )

        self.assertEqual(submit_response.status_code, 400)
