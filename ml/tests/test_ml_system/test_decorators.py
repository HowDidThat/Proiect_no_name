# tests/test_ml_system/test_decorators.py
import pytest
from unittest.mock import Mock, patch
from ml_system.utils.decorators import log_execution_time, clean_and_validate_data
import time


def test_log_execution_time():

    @log_execution_time
    def dummy_function():
        time.sleep(0.1)
        return "test"

    with patch('builtins.print') as mock_print:
        result = dummy_function()

        assert result == "test"
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "Execution time for dummy_function" in call_args


def test_clean_and_validate_data():

    @clean_and_validate_data
    def dummy_function(*args, **kwargs):
        return kwargs.get('payload')

    mock_payload = Mock()
    mock_payload.symptoms = ['High  Fever', 'Sore    Throat']

    result = dummy_function(payload=mock_payload)
    assert result.symptoms == ['high__fever', 'sore____throat']

    mock_payload.symptoms = []
    result = dummy_function(payload=mock_payload)
    assert result.symptoms == []