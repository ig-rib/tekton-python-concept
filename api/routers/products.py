import math
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.interfaces.edit_product_interface import EditProductInterface
from api.interfaces.create_product_interface import CreateProductInterface
from api.interfaces.list_interfaces import SearchableListInterface
from api.services.products import ProductsService, get_products_service

products_router = APIRouter()

@products_router.get("/", status_code=200)
def list_products(products_service: ProductsService = Depends(get_products_service), limit: Optional[int] = 10, page: Optional[int] = 1, q: Optional[str] = None):
    list_parameters = SearchableListInterface(
        limit=limit,
        offset=limit * (page - 1),
        q=q
    )
    products = products_service.get_products(list_parameters)
    return { "items": products, "page": page, "limit": limit }

@products_router.get("/{id}", status_code=200)
def get_product(id: int, products_service: ProductsService = Depends(get_products_service)):
    product = products_service.get_product_by_id(id)
    return product

@products_router.patch("/{id}", status_code=202)
def update_product(id: int, product_params: EditProductInterface, products_service: ProductsService = Depends(get_products_service)):
    updated_product = products_service.edit_product(id, product_params)
    return updated_product

@products_router.post("/", status_code=201)
def create_product(product_params: CreateProductInterface, products_service: ProductsService = Depends(get_products_service)):
    updated_product = products_service.create_product(product_params)
    return updated_product
