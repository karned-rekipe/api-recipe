from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

class ItemCreate(Item):
    id: UUID = Field(default_factory=uuid4, alias="_id")
