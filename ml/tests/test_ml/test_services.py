# tests/test_ml/test_services.py
import pytest
import requests
from unittest.mock import patch, Mock
from django.conf import settings
from ml.api.services import send_to_backend
from ml.api.auth import ApiAuth


@pytest.fixture
def mock_settings(settings):
    settings.BACKEND_API_URL = 'http://test-backend.com'
    return settings


def test_send_to_backend_exists():
    assert callable(send_to_backend)


@patch('ml.api.services.requests.post')
def test_send_to_backend_success(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8, "Disease2": 0.2}
    expected_response = {"status": "success"}

    mock_response = Mock()
    mock_response.json.return_value = expected_response
    mock_post.return_value = mock_response

    result = send_to_backend(quiz_id, predictions)

    assert result == expected_response
    mock_post.assert_called_once()


@patch('ml.api.services.requests.post')
def test_send_to_backend_connection_error(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}
    mock_post.side_effect = requests.ConnectionError()

    result = send_to_backend(quiz_id, predictions)

    assert result is None


@patch('ml.api.services.requests.post')
def test_send_to_backend_timeout(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}
    mock_post.side_effect = requests.Timeout()

    result = send_to_backend(quiz_id, predictions)

    assert result is None


@patch('ml.api.services.requests.post')
def test_send_to_backend_invalid_json(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}

    mock_response = Mock()
    mock_response.json = Mock(side_effect=ValueError("Invalid JSON"))
    mock_post.return_value = mock_response

    result = send_to_backend(quiz_id, predictions)

    assert result is None
    mock_post.assert_called_once_with(
        f"{settings.BACKEND_API_URL}/quiz/{quiz_id}",
        json={'predictions': predictions},
        headers={
            'Authorization': ApiAuth.create_token(),
            'Content-Type': 'application/json'
        },
        timeout=10
    )

@patch('ml.api.services.requests.post')
def test_send_to_backend_empty_predictions(mock_post):
    quiz_id = 123
    predictions = {}

    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    result = send_to_backend(quiz_id, predictions)

    assert result == {"status": "success"}
    mock_post.assert_called_once()


@patch('ml.api.services.requests.post')
def test_send_to_backend_request_exception(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}
    mock_post.side_effect = requests.RequestException()

    result = send_to_backend(quiz_id, predictions)

    assert result is None


@patch('ml.api.services.requests.post')
def test_send_to_backend_invalid_response(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}

    mock_response = Mock()
    mock_response.json.return_value = None
    mock_post.return_value = mock_response

    result = send_to_backend(quiz_id, predictions)

    assert result is None


@patch('ml.api.services.requests.post')
def test_send_to_backend_with_auth(mock_post):
    quiz_id = 123
    predictions = {"Disease1": 0.8}
    auth_token = ApiAuth.create_token()

    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    result = send_to_backend(quiz_id, predictions)

    assert result == {"status": "success"}
    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args[1]
    assert 'headers' in call_kwargs
    assert 'Authorization' in call_kwargs['headers']
    assert call_kwargs['headers']['Authorization'] == auth_token