from .auth_database import engine, Base
from . import models

## Create all database tables
Base.metadata.create_all(bind=engine)
