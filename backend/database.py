# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

# Database URL - Replace this with your actual database URL
DATABASE_URL = "sqlite:///./test.db"  # Example using SQLite. Change for other databases.

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Add other arguments for other DBs.

# Create SessionLocal class that will provide database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the base class for our ORM models
Base = declarative_base()

# Define User model (table)
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
