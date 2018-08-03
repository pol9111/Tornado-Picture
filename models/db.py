from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '192.168.1.8'
PORT = '3306'
DATEBASE = 'tor'
USERNAME = 'admin'
PASSEORD = 'Root110qwe'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSEORD, HOST, PORT, DATEBASE
)

engine = create_engine(DB_URI)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)







