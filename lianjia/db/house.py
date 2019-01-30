from sqlalchemy import Column, String, Integer, DateTime
from db import Base


class HouseModel(Base):
    """链家租房的Model
    """
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    # 户型
    house_type = Column(String(64))
    # 面积
    area = Column(String(32))
    # 租金
    rent = Column(Integer)
    # 地址
    location = Column(String(64))
    # 标签
    label = Column(String(32))
    # 楼层
    floor = Column(String(16))
    # 房源发布时间
    release_time = Column(DateTime)
    # 租期
    rent_period = Column(String(32))
    # 入住时间
    check_in = Column(String(32))
    # 看房时间
    house_view_time = Column(String(32))
