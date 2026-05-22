from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Correct path - data folder is in project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes to S.A.G.E/
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'sage.db')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

print(f"✅ Database connected: {DATABASE_URL}")