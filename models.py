from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    false
)
from database import Base
from sqlalchemy.orm import relationship
import datetime

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    category = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    is_pinned = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=false()
    )

    last_opened_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="prompts"
    )

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    prompts = relationship(
        "Prompt",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
