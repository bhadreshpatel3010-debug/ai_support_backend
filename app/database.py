import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import Base


load_dotenv()  # Load environment variables from .env file
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))  # Ensure pgvector extension is available
        conn.commit()  # Commit the transaction to create the extension
    Base.metadata.create_all(bind=engine)  # Create tables based on models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()