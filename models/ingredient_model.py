from typing import Optional

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = Field(None, description="Quantity of the ingredient")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., g, pcs)")
    created_by: Optional[str] = Field(None, description="User who created this ingredient")