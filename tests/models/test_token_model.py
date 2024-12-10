import pytest
from pydantic import ValidationError

from models.token_model import Token


def test_token_creation():
    token_data = {
        "access_token": "example_access_token",
        "token_type": "Bearer"
    }
    token = Token(**token_data)
    assert token.access_token == "example_access_token"
    assert token.token_type == "Bearer"


def test_token_validation_error():
    invalid_token_data = {
        "access_token": "example_access_token",
        "token_type": 123
    }
    with pytest.raises(ValidationError):
        Token(**invalid_token_data)


def test_token_missing_fields():
    incomplete_token_data = {
        "access_token": "example_access_token"
    }
    with pytest.raises(ValidationError):
        Token(**incomplete_token_data)
