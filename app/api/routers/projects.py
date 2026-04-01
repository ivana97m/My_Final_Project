from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DB
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectFullResponse,
    ProjectInfoResponse,
    ProjectUpdateRequest,
)
from app.services.project_service import project_service

router = APIRouter(prefix="/projects", tags=["projects"]) # za vise projekata
project_router = APIRouter(prefix="/project", tags=["projects"]) # za konkretan projekat


@router.post("", response_model=ProjectInfoResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreateRequest, db: DB, current_user: CurrentUser) -> ProjectInfoResponse:
    project = await project_service.create_project(db, data, current_user)
    return ProjectInfoResponse.model_validate(project)


@router.get("", response_model=list[ProjectFullResponse])
async def list_projects(db: DB, current_user: CurrentUser) -> list[ProjectFullResponse]:
    projects = await project_service.get_accessible_projects(db, current_user)
    return [ProjectFullResponse.model_validate(p) for p in projects]


@project_router.get("/{project_id}/info", response_model=ProjectInfoResponse)
async def get_project_info(project_id: int, db: DB, current_user: CurrentUser) -> ProjectInfoResponse:
    project = await project_service.get_project_with_access_check(db, project_id, current_user)
    return ProjectInfoResponse.model_validate(project)


@project_router.put("/{project_id}/info", response_model=ProjectInfoResponse)
async def update_project_info(
    project_id: int, data: ProjectUpdateRequest, db: DB, current_user: CurrentUser
) -> ProjectInfoResponse:
    project = await project_service.update_project(db, project_id, data, current_user)
    return ProjectInfoResponse.model_validate(project)

