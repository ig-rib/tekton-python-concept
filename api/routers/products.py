from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.models.product import ProductDAO
from api.services.products import ProductsService, get_products_service


products_router = APIRouter()

@products_router.get("/", status_code=200)
def main_status_check(products_service: ProductsService = Depends(get_products_service)):
    products = products_service.get_products()
    return { "products": products }