from datetime import datetime

from sqlalchemy import (
    DATETIME,
    TIMESTAMP,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import User


class Blog(Base):

    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # author = (relationship("User", back_populates="blogs"))
