from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = 'xiaotiepi'
USERPASSWORD = '12580'
HOST = '127.0.0.1'
PORT = '3306'
DBNAME = 'lianjia_house'

# 创建所有model都要复用的基类、数据库链接、Session类
LINK_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, USERPASSWORD, HOST, PORT, DBNAME)
engine = create_engine(LINK_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)