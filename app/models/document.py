from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from ..db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_name: Mapped[str] = mapped_column(String(100), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False, default=0)
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="documents",
    )