from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectInfoResponse
from app.models.users import User
from app.models.projects import Project
from app.models.project_user import ProjectUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class ProjectService:
    async def create_project(self, db: AsyncSession, data: ProjectCreateRequest, owner: User):
        project = Project(name=data.name, description=data.description, owner_id=owner.id)
        db.add(project)
        await db.flush()
        membership = ProjectUser(project_id=project.id, user_id=owner.id)
        db.add(membership)
        await db.refresh(project)
        return project
    async def get_accessible_projects(self, db: AsyncSession, user: User) -> list[Project]:
        result = await db.execute(
            select(Project)
            .join(ProjectUser, ProjectUser.project_id == Project.id)
            .where(ProjectUser.user_id == user.id)
            .order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())


project_service = ProjectService()