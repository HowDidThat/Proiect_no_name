import os
from unittest.mock import patch, Mock

from django.conf import settings
from django.test import TestCase
from ninja.testing import TestClient

from authentication.models import User
from authentication.views import create_tokens
from quiz.models import Quiz, UserQuizProgress
from quiz.utils import generate_random_symptoms, generate_quiz_questions
from quiz.views import quiz_router

os.environ.setdefault('SECRET_KEY', 'pisica')
os.environ.setdefault('SHARED_SECRET_KEY', 'pinguin')


class QuizUtilsTests(TestCase):
    def test_generate_random_symptoms_success(self):
        for num_symptoms in [1, 2, 3]:
            symptoms = generate_random_symptoms(num_symptoms)
            self.assertEqual(len(symptoms), num_symptoms)
            self.assertTrue(all(isinstance(s, str) for s in symptoms))
            self.assertEqual(len(set(symptoms)), num_symptoms)

    def test_generate_random_symptoms_invalid_input(self):
        with self.assertRaises(ValueError):
            generate_random_symptoms(0)

        with self.assertRaises(ValueError):
            generate_random_symptoms(-1)

    @patch('quiz.utils.generate_random_symptoms')
    def test_generate_quiz_questions_success(self, mock_generate_symptoms):
        mock_generate_symptoms.side_effect = [
            ["fever"],
            ["cough"],
            ["headache"],
            ["fatigue"],
            ["nausea"]
        ]

        mock_ml_func = Mock()
        mock_ml_func.side_effect = [
            {
                "predictions": {
                    "flu": 0.8,
                    "covid": 0.6
                }
            },
            {
                "predictions": {
                    "pneumonia": 0.7,
                    "bronchitis": 0.5
                }
            },
            {
                "predictions": {
                    "migraine": 0.9,
                    "stress": 0.4
                }
            },
            {
                "predictions": {
                    "chronic_fatigue": 0.85,
                    "depression": 0.3
                }
            },
            {
                "predictions": {
                    "gastritis": 0.75,
                    "food_poisoning": 0.45
                }
            }
        ]

        questions = generate_quiz_questions(mock_ml_func)

        self.assertEqual(len(questions), 5)
        for question in questions:
            self.assertIn('symptoms', question)
            self.assertIn('diseases', question)
            self.assertTrue(len(question['symptoms']) >= 1)
            self.assertTrue(len(question['diseases']) > 0)

    @patch('quiz.utils.generate_random_symptoms')
    def test_generate_quiz_questions_ml_failure(self, mock_generate_symptoms):
        mock_generate_symptoms.return_value = ["fever"]

        mock_ml_func = Mock()
        mock_ml_func.return_value = None

        with self.assertRaises(Exception) as context:
            generate_quiz_questions(mock_ml_func)

        self.assertIn("Failed to generate questions", str(context.exception))

    @patch('quiz.utils.generate_random_symptoms')
    def test_generate_quiz_questions_not_enough_diseases(self, mock_generate_symptoms):
        mock_generate_symptoms.return_value = ["fever"]

        mock_ml_func = Mock()
        mock_ml_func.return_value = {
            "predictions": {
                "flu": 0.8
            }
        }

        with self.assertRaises(Exception) as context:
            generate_quiz_questions(mock_ml_func)

        self.assertIn("Failed to generate questions", str(context.exception))

    @patch('quiz.utils.generate_random_symptoms')
    def test_generate_quiz_questions_invalid_ml_response(self, mock_generate_symptoms):
        mock_generate_symptoms.return_value = ["fever"]

        mock_ml_func = Mock()
        mock_ml_func.return_value = {"invalid_key": "invalid_value"}

        with self.assertRaises(Exception) as context:
            generate_quiz_questions(mock_ml_func)

        self.assertIn("Failed to generate questions", str(context.exception))


class QuizTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        settings.SECRET_KEY = os.getenv('SECRET_KEY')
        settings.SHARED_SECRET_KEY = os.getenv('SHARED_SECRET_KEY')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            institution='Test Hospital',
            year_of_study=3
        )

        self.access_token, self.refresh_token = create_tokens(self.user.id)
        self.client = TestClient(quiz_router)
        self.user_headers = {"Authorization": f"Bearer {self.access_token}"}

        self.test_questions = [
            {
                "symptoms": ["fever"],
                "diseases": {"flu": 0.8, "covid": 0.6}
            },
            {
                "symptoms": ["cough"],
                "diseases": {"pneumonia": 0.7}
            }
        ]

        self.test_quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Test Description",
            quiz_type="disease_to_symptoms",
            difficulty="easy",
            created_by=self.user,
            questions=self.test_questions
        )

    def test_get_quizzes_success(self):
        response = self.client.get("/", headers=self.user_headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        quiz_data = data[0]
        self.assertEqual(quiz_data['title'], self.test_quiz.title)
        self.assertEqual(quiz_data['description'], self.test_quiz.description)
        self.assertEqual(quiz_data['quiz_type'], self.test_quiz.quiz_type)
        self.assertEqual(quiz_data['difficulty'], self.test_quiz.difficulty)
        self.assertEqual(quiz_data['created_by'], self.user.username)
        self.assertEqual(quiz_data['questions'], self.test_questions)

    def test_get_quiz_by_id_success(self):
        response = self.client.get(f"/{self.test_quiz.id}", headers=self.user_headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], self.test_quiz.title)
        self.assertEqual(data['description'], self.test_quiz.description)
        self.assertEqual(data['quiz_type'], self.test_quiz.quiz_type)
        self.assertEqual(data['difficulty'], self.test_quiz.difficulty)
        self.assertEqual(data['created_by'], self.user.username)
        self.assertEqual(data['questions'], self.test_questions)

    def test_get_quiz_not_found(self):
        non_existent_id = 99999
        response = self.client.get(f"/{non_existent_id}", headers=self.user_headers)
        self.assertEqual(response.status_code, 404)

    @patch('quiz.views.generate_quiz_questions')
    @patch('quiz.views.get_ml_prediction')
    def test_create_quiz_success(self, mock_ml, mock_generate):
        mock_questions = [
            {
                "symptoms": ["fever"],
                "diseases": {"flu": 0.8, "covid": 0.6}
            },
            {
                "symptoms": ["cough", "fatigue"],
                "diseases": {"pneumonia": 0.7, "bronchitis": 0.5}
            }
        ]

        mock_generate.return_value = mock_questions
        mock_ml.return_value = {"predictions": {"flu": 0.8, "covid": 0.6}}

        payload = {
            'title': 'New Quiz',
            'description': 'New Description',
            'quiz_type': 'disease_to_symptoms',
            'difficulty': 'medium'
        }

        response = self.client.post(
            "/",
            json=payload,
            headers=self.user_headers
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['description'], payload['description'])
        self.assertEqual(data['quiz_type'], payload['quiz_type'])
        self.assertEqual(data['difficulty'], payload['difficulty'])
        self.assertEqual(data['created_by'], self.user.username)
        self.assertEqual(data['questions'], mock_questions)

    @patch('quiz.views.generate_quiz_questions')
    @patch('quiz.views.get_ml_prediction')
    def test_create_quiz_failure(self, mock_ml, mock_generate):
        mock_generate.side_effect = Exception("Failed to generate questions")
        mock_ml.return_value = None

        payload = {
            'title': 'Failed Quiz',
            'description': 'Description',
            'quiz_type': 'disease_to_symptoms',
            'difficulty': 'easy'
        }

        response = self.client.post(
            "/",
            json=payload,
            headers=self.user_headers
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Failed to generate questions')

    def test_unauthorized_access(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 401)

        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get("/", headers=invalid_headers)
        self.assertEqual(response.status_code, 401)

    def test_submit_quiz_success(self):
        payload = {
            "answers": [
                {"answer": ["fever"]},
                {"answer": ["pneumonia"]}
            ]
        }

        response = self.client.post(
            f"/{self.test_quiz.id}/submit",
            json=payload,
            headers=self.user_headers
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('score', data)
        self.assertIsInstance(data['score'], (int, float))

        quiz_progress = UserQuizProgress.objects.get(
            user=self.user,
            quiz=self.test_quiz
        )

        self.assertIsNotNone(quiz_progress)
        self.assertEqual(quiz_progress.answers, payload['answers'])
        self.assertEqual(quiz_progress.score, data['score'])
