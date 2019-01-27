from lagou_spider.db.base import engine, Base
"""
创建数据库表
"""
Base.metadata.create_all(engine)