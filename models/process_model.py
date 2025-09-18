from typing import Optional, List

from pydantic import BaseModel, Field

from models.ingredient_model import Ingredient
from models.step_model import StepWrite, StepRead

__all__ = ["ProcessRead", "ProcessWrite"]


class ProcessBase(BaseModel):
    """Base model for a process within a recipe.

    Best practices applied:
    - Shared fields are centralized in a base class to avoid duplication.
    - Extra/unknown fields are ignored for forward compatibility.
    - Explicit typing with sensible defaults for list fields.
    """

    name: Optional[str] = Field(None, description="Optional name for this process")
    recipe_uuid: Optional[str] = Field(None, description="UUID of the recipe this process belongs to")
    utensils: List[str] = Field(default_factory=list, description="List of utensils needed for the recipe")
    ingredients: List[Ingredient] = Field(
        default_factory=list,
        description="List of ingredients with their quantities",
    )


class ProcessRead(ProcessBase):
    """Representation of a process when reading from the API/DB."""

    steps: List[StepRead] = Field(default_factory=list, description="List of steps to prepare the recipe")


class ProcessWrite(ProcessBase):
    """Payload model for creating/updating a process."""

    steps: List[StepWrite] = Field(default_factory=list, description="List of steps to prepare the recipe")
