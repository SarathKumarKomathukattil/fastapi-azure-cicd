from auth.auth_database import engine, Base
from auth import models

## Create all database tables
Base.metadata.create_all(bind=engine)
