from sqlalchemy import create_engine  # create connection to database
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

##Creates Database connection
engine = create_engine(DATABASE_URL)

##Creates a Session
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


##Opening and closing Session
def get_db():
    db = SessionLocal()
    try:
        yield db  ##Use try instead of return,otherwise function end immediately.
    finally:
        db.close()


##Base
Base = declarative_base()
