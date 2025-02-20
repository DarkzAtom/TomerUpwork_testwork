from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    model for User
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="author")
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    """
    model for Post
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
    created_at = Column(DateTime, default=datetime.utcnow) 