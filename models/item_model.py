from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from models.ingredient_model import Ingredient
from models.step_model import Step

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
    created_by: Optional[str] = Field(None, description="User who created the recipe")
