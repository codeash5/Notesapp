from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings

# Creates the actual connection pool to PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Factory that creates new sessions — not a session itself
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class — every ORM model will inherit from this
class Base(DeclarativeBase):
    pass

# Dependency — FastAPI calls this for every request that needs DB
def get_db():
    db = SessionLocal()
    try:
        yield db        # request uses db here
    finally:
        db.close()      # runs even if the route crashes