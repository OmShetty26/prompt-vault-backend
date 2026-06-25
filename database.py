from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. The SQLite database file will be created right inside this folder
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:omshlok123@localhost:5432/promptvault"

# 2. Create the Engine (connect_args is a special requirement just for SQLite)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Create a Session Local class (This is the factory that makes database sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class that our models will inherit from
Base = declarative_base()

# 5. A Dependency function we will use later in main.py to grab a database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()