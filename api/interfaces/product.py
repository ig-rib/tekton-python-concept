from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    status: str
    stock: int
    description: str
    price: int
