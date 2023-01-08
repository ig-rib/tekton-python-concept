
from fastapi import Depends
import redis
from api.database.database import get_db
from api.data_access_objects.product import ProductDAO
from api.interfaces.product import Product
from api.repository.baseRepository import BaseRepository
from sqlalchemy.orm import Session
from api.database.redis import get_redis_db, set_dictionary_values


class ProductsRepository(BaseRepository):
    
    def __init__(self, db: Session=Depends(get_db), redis_db: redis.Redis=Depends(get_redis_db)):
        super().__init__(db=db)
        self.__entity_type__ = ProductDAO
        self.redis_db = redis_db

    def __dao_to_model__(self, dao: ProductDAO) -> Product:
        if not dao: return None
        if not self.redis_db.hmget('status_names', keys=[dao.status])[0]:
            set_dictionary_values()
        status = self.redis_db.hmget('status_names',keys=[dao.status])[0]
        product_model: Product = Product(
            id = dao.id,
            name = dao.name,
            description = dao.description,
            status = status, # map status using cache
            price = dao.price,
            stock = dao.stock
        )

        return product_model

    def __model_to_dao__(self, model: Product) -> ProductDAO:
        if not model: return None
        return ProductDAO(
            id=model.id,
            name=model.name,
            description=model.description,
            status=1,# map status using cache
            price=model.price,
            stock=model.stock
        )

    def find_all(self, limit: int, offset: int, q: str=None):
        ids_query = self.db.query(self.__entity_type__)
        if q:
            ids_query = ids_query.filter(self.__entity_type__.name.ilike(q))
        ids = [x.id for x in ids_query.with_entities(self.__entity_type__.id).offset(offset).limit(limit).all()]
        aux_query = self.db.query(self.__entity_type__)
        entity_daos = aux_query.filter(ProductDAO.id.in_(ids)).all()
        return [self.__dao_to_model__(entity_dao) for entity_dao in entity_daos]

    def find_by_name(self, name: str):
        product = self.db.query(self.__entity_type__).filter(self.__entity_type__.name == name).first()
        return self.__dao_to_model__(product)

    def get_transaction(self):
        return self.db.get_transaction()

def get_products_repository(db: Session = Depends(get_db), redis_db = Depends(get_redis_db)):
    return ProductsRepository(db=db, redis_db=redis_db)