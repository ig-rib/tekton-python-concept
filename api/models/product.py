from sqlalchemy import Column, Integer, String, ForeignKey
from api.database import Base

class ProductDAO(Base):

    __tablename__ = 'products'

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String(256), nullable=False)
    status= Column(Integer, nullable=False)
    stock= Column(Integer, nullable=False)
    description= Column(String(1024), nullable=True)
    price= Column(Integer, nullable=False)

