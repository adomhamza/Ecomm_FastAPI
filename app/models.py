from sqlalchemy import INTEGER, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    image = Column(String, nullable=True)
    user_id = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(
        INTEGER, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(INTEGER, ForeignKey("users.id"), primary_key=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
