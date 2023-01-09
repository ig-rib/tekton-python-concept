from sqlalchemy.orm import Session
from api.database.database import Base

class BaseRepository:

    __entity_type__ = Base

    def __init__(self, db: Session):
        self.db = db

    def save(self, model):
        entity_dao = self.__model_to_dao__(model)
        print(entity_dao)
        self.db.add(entity_dao)
        self.db.commit()
        return self.__dao_to_model__(entity_dao)

    def update(self, model):
        entity_dao = self.__model_to_dao__(model)
        self.db.flush(entity_dao)
        self.db.commit()

    def __dao_to_model__(self, dao):
        raise NotImplementedError()

    def __model_to_dao__(self, model):
        raise NotImplementedError()

    def find_by_id(self, id_):
        entity_dao = self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).first()
        return self.__dao_to_model__(entity_dao)

    def find_all(self, limit=None, offset=None):
        entity_daos = self.db.query(self.__entity_type__).offset(offset, limit).all()
        return [self.__dao_to_model__(entity_dao) for entity_dao in entity_daos]

    def delete_by_id(self, id_):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).remove()