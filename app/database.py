from sqlalchemy import create_engine # rngine make connection to postgres
from sqlalchemy.orm import sessionmaker, declarative_base # factory for database & base clss for ORM models

DATABASE_URL = "postgresql://user:password@localhost:5432/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()