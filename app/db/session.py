from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)  # connection with the database

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # run query inside the database


def get_db():  # give session to fastapi during request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
