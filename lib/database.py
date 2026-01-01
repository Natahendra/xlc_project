import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# Load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

def get_session():
    with Session(engine) as session:
        yield session
