
import json
from fastapi import Depends, HTTPException
from api.interfaces.editProductInterface import EditProductInterface
from api.repository.productRepository import ProductsRepository
from api.repository.productRepository import get_products_repository

class ProductsService:

    products_repository: ProductsRepository

    def __init__(self, products_repository: ProductsRepository):
        print('Initializing products service with products repository')
        self.products_repository = products_repository

    def get_products(self):
        return self.products_repository.find_all()

    def get_product_by_id(self, id):
        product = self.products_repository.find_by_id(id)
        if not product:
            raise HTTPException(status_code=404, detail=f'Product not found for id {id}')

    def edit_product(self, id, params: EditProductInterface):
        product = self.get_product_by_id(id)
        if params.name: product.name = params.name
        if params.description: product.description = params.description
        if params.status: product.status = params.status
        if params.stock: product.stock = params.stock
        if params.price: product.price = params.price

        self.products_repository.save(product)

        


def get_products_service(products_repository: ProductsRepository = Depends(get_products_repository)) -> ProductsService:
    return ProductsService(products_repository)