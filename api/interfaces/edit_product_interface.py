from typing import Literal, Optional
from pydantic import BaseModel

class EditProductInterface(BaseModel):
    name: Optional[str]
    status: Optional[Literal['Active', 'Inactive']]
    stock: Optional[int]
    description: Optional[str]
    price: Optional[int]
