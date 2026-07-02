from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id            = Column(Integer, primary_key=True, index=True)
    session_id    = Column(String, index=True, nullable=False)
    role          = Column(String, nullable=False)      
    content       = Column(Text, nullable=False)
    category      = Column(String, nullable=True)        
    sentiment     = Column(String, nullable=True)        
    created_at    = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Create all tables if they don't exist"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to create tables | error={e}")
        raise

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()