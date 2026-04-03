from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DB
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectInfoResponse,
)
from app.services.project_service import project_service

router = APIRouter(prefix="/projects", tags=["projects"])



@router.post("", response_model=ProjectInfoResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreateRequest, db: DB, current_user: CurrentUser) -> ProjectInfoResponse:
    project = await project_service.create_project(db, data, current_user)
    return ProjectInfoResponse.model_validate(project)


@router.get("", response_model=list[ProjectInfoResponse])
async def list_projects(db: DB, current_user: CurrentUser) -> list[ProjectInfoResponse]:
    projects = await project_service.get_accessible_projects(db, current_user)
    return [ProjectInfoResponse.model_validate(p) for p in projects]

