
import json
from typing import Optional
from fastapi import Depends, HTTPException
from api.interfaces.create_product_interface import CreateProductInterface
from api.interfaces.edit_product_interface import EditProductInterface
from api.interfaces.list_interfaces import SearchableListInterface
from api.interfaces.product import Product
from api.repository.productRepository import ProductsRepository
from api.repository.productRepository import get_products_repository

class ProductsService:

    products_repository: ProductsRepository

    def __init__(self, products_repository: ProductsRepository):
        print('Initializing products service with products repository')
        self.products_repository = products_repository

    def get_products(self, filters: Optional[SearchableListInterface]):
        return self.products_repository.find_all(filters.limit, filters.offset, filters.q)

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

        updated_product = self.products_repository.save(product)
        return updated_product

    def create_product(self, params: CreateProductInterface):
        existing_product = self.products_repository.find_by_name(params.name)
        if existing_product:
            raise HTTPException(status_code=400, detail=f'Product with name {params.name} already exists.')
        new_product_model = Product(
            id=None,
            name=params.name,
            status=params.status,
            stock=params.stock,
            description=params.description,
            price=params.price
        )

        new_product = self.products_repository.save(new_product_model)
        return new_product

def get_products_service(products_repository: ProductsRepository = Depends(get_products_repository)) -> ProductsService:
    return ProductsService(products_repository)