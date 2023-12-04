from typing import Union

from icecream import ic
from datetime import datetime
from fastapi import HTTPException, status

from recipe.models.recipe import ModelRecipe


class Recipe:
    DB_DBMS = 'MongoDB'
    DB_CONTAINER = 'recipe'

    def __init__(self, recipe: Union[ModelRecipe, dict]):
        if isinstance(recipe, ModelRecipe):
            self._id: str = recipe.id
            self.label: str = recipe.label
            self.start: datetime = recipe.start
            self.end: datetime = recipe.end
        elif isinstance(recipe, dict):
            self._id: str = recipe.get('id')
            self.label: str = recipe.get('label')
            self.start: datetime = recipe.get('start')
            self.end: datetime = recipe.get('end')
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Invalid recipe type. Expected ModelRecipe or dict."
                }
            )

        self.status: str = self.get_status()

    def get_status(self, date=None) -> str:
        if date is None:
            reference = datetime.now().date()
        else:
            reference = datetime.strptime(date, '%Y-%m-%d').date()

        start = self.start.date() if self.start is not None else None
        end = self.end.date() if self.end is not None else None

        if date is not None:
            reference = date

        if start is None and end is None:
            return "Active"
        elif start is not None and end is None:
            return "Active" if start <= reference else "Inactive"
        elif start is None and end is not None:
            return "Active" if end >= reference else "Inactive"
        elif start is not None and end is not None:
            return "Active" if start <= reference <= end else "Inactive"

        return 'Inactive'
