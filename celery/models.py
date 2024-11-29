# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL
DATABASE_URL = "sqlite:///posts.db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Data Model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)