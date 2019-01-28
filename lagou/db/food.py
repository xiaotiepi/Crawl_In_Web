from sqlalchemy import Column, String, Integer
from db import Base


class FoodModel(Base):
    """大众点评的Model
    """

    __tablename__ = 'food'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    per_consume = Column(Integer)
    comment_num = Column(Integer)
    address = Column(String(128))
    taste_score = Column(Integer)
    environment_score = Column(Integer)
    service_score = Column(Integer)
    dishes = Column(String(128))
