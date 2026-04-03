from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from ..db.base import Base
from enum import Enum


class ProjectRole(str, Enum):
    OWNER = "owner"
    PARTICIPANT = "participant"

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int]=mapped_column(primary_key=True, index=True)
    name: Mapped[str]=mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None]=mapped_column(String(500), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    total_size_bytes: Mapped[int]=mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="owned_projects",
        cascade="all, delete")

    members: Mapped[list["ProjectUser"]] = relationship(
        "ProjectUser",
        back_populates="project",
        cascade="all, delete-orphan")




