from ctypes import Union
from typing import Optional
from pydantic import BaseModel
from api.interfaces.product import Product
from api.serializers.base_serializer import BaseSerializer
from api.serializers.product_serializer import ProductDTO


class CompleteProductSerializer(BaseSerializer):
    def serialize(self, model: Product):
        return CompleteProductDTO(
            id=model.id,
            name=model.name,
            status=model.status,
            stock=model.stock,
            description=model.description,
            price=model.price,
            discount=model.discount,
            final_price=model.price * (100 - model.discount) / 100
        )

class CompleteProductDTO(ProductDTO):
    discount: int
    final_price: int