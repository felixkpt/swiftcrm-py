# app/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection configuration
from decouple import Config, RepositoryEnv

DOTENV_FILE = '.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

DB_HOST = env_config.get('DB_HOST')
DB_USER = env_config.get('DB_USER')
DB_PASS = env_config.get('DB_PASS')
DB_NAME = env_config.get('DB_NAME')
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

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
