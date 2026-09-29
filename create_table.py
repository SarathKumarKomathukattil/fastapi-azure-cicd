from database import engine,Base
import model

## Create all database tables 
Base.metadata.create_all(bind=engine)


