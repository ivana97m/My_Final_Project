from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectInfoResponse
from app.models.users import User
from app.models.projects import Project
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectService:
    async def create_project(self, db: AsyncSession, data: ProjectCreateRequest, owner: User):
        project = Project(name=data.name, description=data.description, owner_id=owner.id)
        db.add(project)
        await db.flush()
        await db.refresh(project)
        return project

