from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Step(BaseModel):
    step_number: int
    description: str
    duration: Optional[str] = Field(None, description="Optional duration for this step (e.g., 10 min)")