from sqlalchemy import Column, String, Integer
from db.base import Base


class JobModel(Base):
    """
    拉钩的职位的Model
    """
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    city = Column(String(16))
    salary_range = Column(String(32))
    experience = Column(String(32))
    education = Column(String(16))
    tags = Column(String(256))
    company = Column(String(32))
    location = Column(String(256))