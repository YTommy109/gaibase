from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.engine.create import create_engine


username = 'USER'
password = 'PASSWORD'
hostname = 'localhost'
dbname = 'DATABASE'
url = URL.create(
    drivername='mysql+mysqlconnector',
    username=username,
    password=password,
    host=hostname,
    database=dbname,
    query={"charset": "utf8"},
)
engine = create_engine(url, pool_recycle=10)

def get_db_session():
    return sessionmaker(bind=engine)()