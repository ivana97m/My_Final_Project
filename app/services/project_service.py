from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectInfoResponse
from app.models.users import User
from app.models.projects import Project
from app.models.project_user import ProjectUser
from app.core.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload




class ProjectService:
    async def create_project(self, db: AsyncSession, data: ProjectCreateRequest, owner: User):
        project = Project(name=data.name, description=data.description, owner_id=owner.id)
        db.add(project)
        await db.flush()
        await db.refresh(project)
        return project
    async def get_accessible_projects(self, db: AsyncSession, user: User) -> list[Project]:
        result = await db.execute(
            select(Project)
            .join(ProjectUser, ProjectUser.project_id == Project.id)
            .where(ProjectUser.user_id == user.id)
            .options(selectinload(Project.documents))
            .order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_project_with_access_check(
        self, db: AsyncSession, project_id: int, user: User
    ) -> Project:
        project = await db.scalar(
            select(Project)
            .where(Project.id == project_id)
            .options(selectinload(Project.documents))
        )
        if not project:
            raise NotFoundException("Project not found")
        await self._check_member(db, project_id, user.id)
        return project
    async def update_project(
        self, db: AsyncSession, project_id: int, data: ProjectUpdateRequest, user: User
    ) -> Project:
        project = await self.get_project_with_access_check(db, project_id, user)
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        await db.flush()
        await db.refresh(project)
        return project

project_service = ProjectService()