import os

from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker 

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
dbschema = "USERMENU"

DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
print(f'DATABASE_URI = {DATABASE_URI}')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# entender melhor
Base = declarative_base()
