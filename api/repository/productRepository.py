
from fastapi import Depends
from api.database.database import get_db
from api.models.product import ProductDAO
from api.repository.baseRepository import BaseRepository
from sqlalchemy.orm import Session

class ProductsRepository(BaseRepository):
    
    def __init__(self, db: Session=Depends(get_db)):
        super().__init__(db=db)
        self.__entity_type__ = ProductDAO


def get_products_repository(db: Session = Depends(get_db)):
    return ProductsRepository(db=db)