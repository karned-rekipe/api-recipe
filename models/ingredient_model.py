from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = Field(None, description="Quantity of the ingredient")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., g, pcs)")