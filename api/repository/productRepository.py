
from fastapi import Depends
from api.database.database import get_db
from api.data_access_objects.product import ProductDAO
from api.interfaces.product import Product
from api.repository.baseRepository import BaseRepository
from sqlalchemy.orm import Session

class ProductsRepository(BaseRepository):
    
    def __init__(self, db: Session=Depends(get_db)):
        super().__init__(db=db)
        self.__entity_type__ = ProductDAO

    def __dao_to_model__(self, dao: ProductDAO) -> Product:
        product_model: Product = Product()
        
        product_model.id = dao.id
        product_model.name = dao.name
        product_model.description = dao.description
        product_model.status = dao.status # map status using cache
        product_model.price = dao.price
        product_model.stock = dao.stock

        return product_model

    def __model_to_dao__(self, model: Product) -> ProductDAO:
        
        product_dao = ProductDAO()
        
        product_dao.id = model.id
        product_dao.name = model.name
        product_dao.description = model.description
        product_dao.status = model.status # map status using cache
        product_dao.price = model.price
        product_dao.stock = model.stock

    def get_transaction(self):
        return self.db.get_transaction()

def get_products_repository(db: Session = Depends(get_db)):
    return ProductsRepository(db=db)