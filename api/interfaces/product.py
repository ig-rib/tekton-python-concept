from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id: Optional[int]
    name: str
    status: str
    stock: int
    description: Optional[str]
    price: int
    discount: Optional[int]

