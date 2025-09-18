from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["StepRead", "StepWrite"]


class StepBase(BaseModel):
    """Base model for a recipe step.

    Best practices applied:
    - No implicit coercion of mixed-type fields like duration; keep user-provided format.
    - Shared fields kept in a base class to avoid duplication.
    - Extra fields ignored to be more resilient to upstream changes.
    """

    step_number: int
    title: Optional[str] = Field(None, description="Optional title for this step")
    # Keep description optional here; override in StepWrite to make it required
    description: Optional[str] = Field(None, description="Description for this step")
    # Keep duration as a free-form string (e.g., "10 min"); callers may parse if needed
    duration: Optional[str] = Field(None, description="Optional duration for this step (e.g., '10 min')")
    created_by: Optional[str] = Field(None, description="User who created this step")
    cooking_time: Optional[int] = Field(None, description="Optional cooking time in seconds for this step")
    rest_duration: Optional[int] = Field(None, description="Optional rest duration in seconds for this step")
    preparation_time: Optional[int] = Field(None, description="Optional preparation time in seconds for this step")



class StepRead(StepBase):
    """Representation of a step when reading from the API/DB."""

    # Keep duration numeric on read models to minimize impact on existing consumers
    duration: Optional[int] = Field(None, description="Optional duration for this step in seconds")


class StepWrite(StepBase):
    """Payload model for creating/updating a step.

    Description is required when writing, while other fields remain optional.
    """

    description: str = Field(..., description="Description for this step")