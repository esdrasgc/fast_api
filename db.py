from sqlmodel import Session, SQLModel, create_engine
import pymysql
import dotenv
import os
## -------------------------- configuração do BD ----------------------------------- ##

dotenv.load_dotenv()
DB_TYPE = os.getenv("DB_TYPE")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_PASSWORD=DB_PASSWORD.replace("@", "%40")
DB_PASSWORD=DB_PASSWORD.replace("/", "%2F")

# mysql_url = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db_connection_url = f'{DB_TYPE}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(db_connection_url)
engine = create_engine(db_connection_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
