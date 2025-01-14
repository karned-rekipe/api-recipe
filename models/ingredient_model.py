from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = Field(None, description="Quantity of the ingredient")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., g, pcs)")

    @validator("quantity", pre = True, always = True)
    def convert_quantity_to_float(cls, value):
        if value is None:
            return value
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Quantity must be a number or convertible to a number, got '{value}'")
