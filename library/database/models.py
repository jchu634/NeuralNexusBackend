from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase, mapped_column

from library.database.database import Base


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"
    id: Mapped[str] = mapped_column(primary_key=True)
    username = Column(String, index=True)
    email = Column(String, nullable=True)
    password_hash = Column(String)
    is_admin = Column(Boolean)
    images: Mapped[list["Image"]] = relationship(back_populates="user")
    settings: Mapped["Setting"] = relationship(back_populates="user")


class Setting(Base):
    __tablename__ = "settings_table"
    id: Mapped[str] = mapped_column(
        ForeignKey("user_table.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="settings")
    image_expiry = Column(Integer)


class Image(Base):
    __tablename__ = "image_table"
    id: Mapped[str] = mapped_column(primary_key=True)
    image_hash = Column(String, index=True)
    image_name = Column(String, index=True)
    expiry_time = Column(Integer, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(
        back_populates="images"
    )
