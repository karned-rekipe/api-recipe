from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = Field(None, description="Quantity of the ingredient")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., g, pcs)")

class Step(BaseModel):
    step_number: int
    description: str
    duration: Optional[str] = Field(None, description="Optional duration for this step (e.g., 10 min)")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    number_of_persons: Optional[int] = Field(None, gt=0, description="Number of persons the recipe serves")
    origin_country: Optional[str] = None
    attributes: List[str] = Field(default_factory=list, description="Attributes like vegetarian, gluten-free, etc.")
    utensils: List[str] = Field(default_factory=list, description="List of utensils needed for the recipe")
    ingredients: List[Ingredient] = Field(default_factory=list, description="List of ingredients with their quantities")
    steps: List[Step] = Field(default_factory=list, description="List of steps to prepare the recipe")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="URL for the recipe thumbnail image")
    large_image_url: Optional[HttpUrl] = Field(None, description="URL for a larger image of the recipe")
    source_reference: Optional[str] = Field(None, description="Reference for the source of the recipe (e.g., book, website)")

