from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.interfaces.editProductInterface import EditProductInterface
from api.data_access_objects.product import ProductDAO
from api.services.products import ProductsService, get_products_service


products_router = APIRouter()

@products_router.get("/", status_code=200)
def list_all_products(products_service: ProductsService = Depends(get_products_service)):
    products = products_service.get_products()
    return { "products": products }

@products_router.get("/{id}", status_code=200)
def get_product(id: int, products_service: ProductsService = Depends(get_products_service)):
    product = products_service.get_product_by_id(id)
    return product

@products_router.patch("/{id}", status_code=201)
def update_product(id: int, product_params: EditProductInterface, products_service: ProductsService = Depends(get_products_service)):
    updated_product = products_service.edit_product(id, product_params)
    return updated_product