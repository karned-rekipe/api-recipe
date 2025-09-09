from typing import Optional

from pydantic import BaseModel, Field


class Step(BaseModel):
    step_number: int
    title: str
    description: str
    duration: Optional[int] = Field(None, description="Optional duration for this step (e.g., 600 sec)")
    created_by: Optional[str] = Field(None, description="User who created this step")
    cooking_time: Optional[int] = Field(None, description="Optional cooking time for this step (e.g., 600 sec)")
    rest_duration: Optional[int] = Field(None, description="Optional rest duration for this step (e.g., 600 sec)")
    preparation_time: Optional[int] = Field(None, description="Optional preparation time for this step (e.g., 600 sec)")