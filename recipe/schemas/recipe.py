from recipe.models import *


class HealthcheckResponse(BaseModel):
    message: str


class SchemaRecipeId(ModelRecipeUlid):
    """Recipe ID schema
    """
    pass


class SchemaRecipeCreate(ModelRecipeDatabaseFields, ModelRecipeUlidOptional):
    """Create recipe schema
    """
    pass


class SchemaRecipeRead(ModelRecipeComputeFields, ModelRecipeDatabaseFields, ModelRecipeUlid):
    """Read recipe schema
    """
    pass


class SchemaRecipeUpdate(ModelRecipeDatabaseFields):
    """Update recipe schema
    """
    pass
