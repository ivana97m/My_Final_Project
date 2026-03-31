class ProjectUser(Base):
    __tablename__ = "project_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped[Project] = relationship(
        "Project",
        back_populates="members",

    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="project_memberships",
        foreign_keys="User.id"

    )
