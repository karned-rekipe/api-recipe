from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class ReadIngredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    created_by: Optional[str] = None

class ReadStep(BaseModel):
    step_number: int
    description: str
    duration: Optional[str] = None
    created_by: Optional[str] = None

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
    ingredients: List[ReadIngredient] = []
    steps: List[ReadStep] = []
    thumbnail_url: Optional[HttpUrl] = None
    large_image_url: Optional[HttpUrl] = None
    source_reference: Optional[str] = None
    created_by: Optional[str] = None
