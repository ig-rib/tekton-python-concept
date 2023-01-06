from pydantic import BaseModel


class ProductDAO(BaseModel):
    product_id: int
    name: str
    status: int
    stock: int
    description: str
    price: int

