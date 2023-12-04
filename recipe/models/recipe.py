from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import ulid


class ModelRecipeUlid(BaseModel):
    id: ulid = Field(
        default_factory = ulid.ulid,
        alias = "_id",
        description = "ULID of recipe",
        example = "01H81Z7W545XNWSP9B4JMRMODC"
    )

    class Config:
        arbitrary_types_allowed = True


class ModelRecipeUlidOptional(BaseModel):
    id: Optional[str] = Field(
        None,
        alias = "_id",
        description = "ULID of recipe (optional)",
        example = "01H81Z7W545XNWSP9B4JMRRRC0"
    )


class ModelRecipeDatabaseFields(BaseModel):
    label: str = Field(
        ...,
        description = "The name of my recipe",
        example = "My recipe name",
        min_length = 1,
        max_length = 50
    )
    start: Optional[datetime] = Field(
        None,
        description = "The date when recipe start to be a recipe",
        example = "2023-11-17 09:00:00",
        min_length = 0,
        max_length = 19
    )
    end: Optional[datetime] = Field(
        None,
        description = "The date when recipe stop to be a recipe",
        example = "2023-11-17 09:00:00",
        min_length = 0,
        max_length = 19
    )


class ModelRecipeComputeFields(BaseModel):
    status: str = Field(
        ...,
        description = "Status of recipe",
        example = "Active"
    )


class ModelRecipe(ModelRecipeDatabaseFields, ModelRecipeUlid):
    pass
