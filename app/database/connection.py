# app/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection configuration
DATABASE_URL = "mysql+mysqlconnector://root:Felix1234!@127.0.0.1/swiftcrm_py"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker object for the ORM session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
