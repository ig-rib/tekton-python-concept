
import json
from fastapi import Depends
from api.repository.productRepository import ProductsRepository
from api.repository.productRepository import get_products_repository

class ProductsService:

    products_repository: ProductsRepository

    def __init__(self, products_repository: ProductsRepository):
        print('Initializing products service with products repository')
        self.products_repository = products_repository

    def get_products(self):
        return self.products_repository.find_all()


def get_products_service(products_repository: ProductsRepository = Depends(get_products_repository)) -> ProductsService:
    return ProductsService(products_repository)