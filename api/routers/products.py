from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.models.product import ProductDAO


products_router = APIRouter()

@products_router.get("/", status_code=200)
def main_status_check(db: Session = Depends(get_db)):
    products = db.query(ProductDAO).all()
    return { "products": products }