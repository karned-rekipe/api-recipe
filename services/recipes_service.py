from fastapi import HTTPException
from models.recipe_model import RecipeWrite, RecipeRead
from models.step_model import StepWrite
from common_api.utils.v0 import get_state_repos
from typing import Optional


def _compute_step_duration(step: StepWrite) -> Optional[int]:
    """
    Compute duration of a step as the sum of cooking_time, rest_duration and preparation_time.
    Treat missing/None values as 0. Returns None if all three are None (keeps duration unset),
    otherwise returns the integer sum.
    """
    ct = step.cooking_time or 0
    rd = step.rest_duration or 0
    pt = step.preparation_time or 0
    if all(v == 0 for v in (ct, rd, pt)):
        return None
    return int(ct + rd + pt)


def _apply_duration_on_steps(recipe: RecipeWrite) -> None:
    """Mutates recipe.steps to ensure duration is computed from component times."""
    for i, st in enumerate(recipe.steps or []):
        duration = _compute_step_duration(st)
        # set computed duration (can be None)
        recipe.steps[i].duration = duration


def create_recipe(request, new_recipe) -> str:
    try:
        # compute duration on all steps before persisting
        _apply_duration_on_steps(new_recipe)
        repos = get_state_repos(request)
        new_uuid = repos.recipe_repo.create_recipe(new_recipe)
        if not isinstance(new_uuid, str):
            raise TypeError("The method create_recipe did not return a str.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the recipe: {e}")

    return new_uuid

def get_recipes(request) -> list[RecipeRead]:
    try:
        repos = get_state_repos(request)
        recipes = repos.recipe_repo.list_recipes()
        if not isinstance(recipes, list):
            raise TypeError("The method list_recipes did not return a list.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get the list of recipes: {e}")

    return recipes


def get_recipe(request, uuid: str) -> RecipeWrite:
    try:
        repos = get_state_repos(request)
        recipe = repos.recipe_repo.get_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the recipe: {e}")

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe

def _apply_duration_on_steps_on_update(recipe_update: RecipeWrite, existing_recipe: dict) -> None:
    """
    For update operations, recompute duration only if cooking_time, rest_duration or preparation_time
    changed compared to the existing recipe. Mutates recipe_update.steps in place.
    """
    existing_steps = existing_recipe.get("steps", []) if isinstance(existing_recipe, dict) else []
    # map by step_number for easy lookup
    idx_by_number = {s.get("step_number"): s for s in existing_steps if isinstance(s, dict)}
    for i, st in enumerate(recipe_update.steps or []):
        old = idx_by_number.get(st.step_number)
        if old is None:
            # New step -> compute duration
            recipe_update.steps[i].duration = _compute_step_duration(st)
            continue
        # Extract previous values
        old_ct = old.get("cooking_time")
        old_rd = old.get("rest_duration")
        old_pt = old.get("preparation_time")
        # If any changed, recompute
        if st.cooking_time != old_ct or st.rest_duration != old_rd or st.preparation_time != old_pt:
            recipe_update.steps[i].duration = _compute_step_duration(st)
        else:
            # keep previous duration as-is if present
            if "duration" in old:
                recipe_update.steps[i].duration = old.get("duration")


def update_recipe(request, uuid: str, recipe_update: RecipeWrite) -> None:
    try:
        repos = get_state_repos(request)
        # fetch existing to compare
        existing = repos.recipe_repo.get_recipe(uuid)
        if existing is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        _apply_duration_on_steps_on_update(recipe_update, existing)
        repos.recipe_repo.update_recipe(uuid, recipe_update)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the recipe: {e}")

def delete_recipe(request, uuid: str) -> None:
    try:
        repos = get_state_repos(request)
        repos.recipe_repo.delete_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the recipe: {e}")