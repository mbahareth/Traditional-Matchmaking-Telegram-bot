"""
Database initialization and connection management for the Traditional Matchmaking Telegram Bot.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from src.config import DB_URI
from src.models import Base

# Create directory for database if it doesn't exist
os.makedirs(os.path.dirname(DB_URI.replace('sqlite:///', '')), exist_ok=True)

# Create database engine
engine = create_engine(DB_URI)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)

def get_session():
    """Get a new database session."""
    return Session()

def close_session(session):
    """Close a database session."""
    session.close()
