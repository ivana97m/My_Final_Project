from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from ..db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)

# user can have multiple projects
    owned_projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="owner",
        foreign_keys= "Project.owner_id",
        cascade="all, delete-orphan"
    )
# sharing projects
    project_memberships: Mapped[list["ProjectMember"]] = relationship(
        "ProjectMember",
        back_populates="user"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"



