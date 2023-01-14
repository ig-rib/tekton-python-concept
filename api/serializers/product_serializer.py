from ctypes import Union
from typing import Optional
from pydantic import BaseModel
from api.interfaces.product import Product
from api.serializers.base_serializer import BaseSerializer


class ProductSerializer(BaseSerializer):
    def serialize(self, model: Product):
        return ProductDTO(
            id=model.id,
            name=model.name,
            status=model.status,
            stock=model.stock,
            description=model.description,
            price=model.price
        )

class ProductDTO(BaseModel):
    id: int
    name: str
    status: str
    stock: int
    description: Optional[str]
    price: int