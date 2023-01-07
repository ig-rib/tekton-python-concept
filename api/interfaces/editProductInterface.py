from typing import Optional
from pydantic import BaseModel

class EditProductInterface(BaseModel):
    name: Optional[str]
    status: Optional[str]
    stock: Optional[int]
    description: Optional[str]
    price: Optional[int]
