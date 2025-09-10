import pytest
from pydantic import ValidationError

from models.step_model import StepWrite


def test_step_creation():
    step_data = {
        "step_number": 1,
        "description": "First step",
        "duration": "10 min"
    }
    step = StepWrite(**step_data)
    assert step.step_number == 1
    assert step.description == "First step"
    assert step.duration == "10 min"


def test_step_creation_without_duration():
    step_data = {
        "step_number": 2,
        "description": "Second step"
    }
    step = StepWrite(**step_data)
    assert step.step_number == 2
    assert step.description == "Second step"
    assert step.duration is None


def test_step_validation_error():
    invalid_step_data = {
        "step_number": "one",
        "description": "Invalid step"
    }
    with pytest.raises(ValidationError):
        StepWrite(**invalid_step_data)


def test_step_missing_fields():
    incomplete_step_data = {
        "step_number": 3
    }
    with pytest.raises(ValidationError):
        StepWrite(**incomplete_step_data)
