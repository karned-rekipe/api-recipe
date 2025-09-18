from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

from models.process_model import ProcessRead, ProcessWrite

__all__ = ["RecipeRead", "RecipeWrite"]


class RecipeBase(BaseModel):
    """Base model for a recipe.

    Best practices applied:
    - Shared fields kept in base class to avoid duplication.
    - Extra/unknown fields ignored for forward compatibility.
    - Explicit typing and defaults for collection fields.
    """

    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    difficulty: Optional[int] = None
    quantity: Optional[int] = None
    number_of_persons: Optional[int] = Field(None, gt=0, description="Number of persons the recipe serves")
    origin_country: Optional[str] = None
    attributes: List[str] = Field(default_factory=list, description="Attributes like vegetarian, gluten-free, etc.")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="URL for the recipe thumbnail image")
    large_image_url: Optional[HttpUrl] = Field(None, description="URL for a larger image of the recipe")
    source_reference: Optional[str] = Field(None, description="Reference for the source of the recipe (e.g., book, website)")
    created_by: Optional[str] = Field(None, description="User who created the recipe")


class RecipeRead(RecipeBase):
    """Representation of a recipe when reading from the API/DB."""

    uuid: str
    process: List[ProcessRead] = Field(default_factory=list, description="List of processes used to prepare the recipe")


class RecipeWrite(RecipeBase):
    """Payload model for creating/updating a recipe."""

    process: List[ProcessWrite] = Field(default_factory=list, description="List of processes used to prepare the recipe")
