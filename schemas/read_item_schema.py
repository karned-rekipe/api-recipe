from pydantic import BaseModel, HttpUrl
from typing import Optional, List

from models.ingredient_model import Ingredient
from models.step_model import Step


class ReadItem(BaseModel):
    uuid: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    number_of_persons: Optional[int] = None
    origin_country: Optional[str] = None
    attributes: List[str] = []
    utensils: List[str] = []
    ingredients: List[Ingredient] = []
    steps: List[Step] = []
    thumbnail_url: Optional[HttpUrl] = None
    large_image_url: Optional[HttpUrl] = None
    source_reference: Optional[str] = None
    created_by: Optional[str] = None
