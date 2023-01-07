from typing import Optional
from pydantic import BaseModel

class CreateProductInterface(BaseModel):
    name: str
    status: str
    stock: int
    description: Optional[str]
    price: int
