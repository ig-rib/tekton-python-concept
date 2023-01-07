from sqlalchemy.orm import Session
from api.database.database import Base

class BaseRepository:

    __entity_type__ = Base

    def __init__(self, db: Session):
        self.db = db

    def save(self, entity):
        self.db.add(entity)
        self.db.commit()

    def find_by_id(self, id_):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).first()

    def find_all(self, limit=None, offset=None):
        return self.db.query(self.__entity_type__).all()

    def delete_by_id(self, id_):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).remove()