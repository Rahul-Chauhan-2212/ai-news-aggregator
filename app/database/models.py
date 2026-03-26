from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String, unique=True)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String)
    published_date = Column(DateTime)  # When article was published
    created_at = Column(DateTime, default=datetime.utcnow)  # When record was created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When record was last updated
    updated_date = Column(DateTime)  # When article content was last updated