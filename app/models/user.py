
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.task import Task
if TYPE_CHECKING:
   
    from app.models.taskassignments import TaskAssignments

    assignments: Mapped[list["TaskAssignments"]] = relationship(
        "TaskAssignments",
        back_populates="user",
        cascade="all, delete-orphan",
    )
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=False,
    )

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    isactive: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
 
    assignments: Mapped[list["TaskAssignments"]] = relationship(
        "TaskAssignments",
        back_populates="user",
        cascade="all, delete-orphan",
    )