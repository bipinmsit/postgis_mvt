from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config.env import DB_CONFIG
import asyncio

# Update DATABASE_URL with your actual database details and SSL certificate path
# Define your database URL
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DB_CONFIG["user"],
    DB_CONFIG["password"],
    DB_CONFIG["host"],
    DB_CONFIG["port"],
    DB_CONFIG["dbname"],
)
engine = create_engine(DATABASE_URL)
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()
