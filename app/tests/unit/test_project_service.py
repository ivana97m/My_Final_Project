from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.projects import Project
from app.models.project_user import ProjectUser
from app.models.users import User
from app.schemas.project import ProjectCreateRequest
from app.services.project_service import ProjectService


def make_user(user_id: int = 1) -> User:
    user = User()
    user.id = user_id
    return user


def make_project(project_id: int = 1) -> Project:
    project = Project()
    project.id = project_id
    project.name = "Test Project"
    project.description = "Test Description"
    project.owner_id = 1
    project.total_size_bytes = 0
    return project


@pytest.fixture
def service() -> ProjectService:
    return ProjectService()


@pytest.fixture
def mock_db() -> AsyncMock:
    db = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.mark.asyncio
async def test_create_project_success(service: ProjectService, mock_db: AsyncMock):
    mock_db.flush = AsyncMock()
    mock_db.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, "id", 1) or None)

    data = ProjectCreateRequest(name="New Project", description="Desc")
    result = await service.create_project(mock_db, data, make_user())

    # Proveri da su dodati Project + ProjectUser
    assert mock_db.add.call_count == 2

    created_project = mock_db.add.call_args_list[0][0][0]
    assert created_project.name == "New Project"
    assert created_project.description == "Desc"
    assert created_project.owner_id == 1

    created_membership = mock_db.add.call_args_list[1][0][0]
    assert isinstance(created_membership, ProjectUser)
    assert created_membership.user_id == 1


@pytest.mark.asyncio
async def test_get_accessible_projects(service: ProjectService, mock_db: AsyncMock):
    projects = [make_project(1), make_project(2)]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = projects
    mock_db.execute.return_value = mock_result

    result = await service.get_accessible_projects(mock_db, make_user())

    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_accessible_projects_empty(service: ProjectService, mock_db: AsyncMock):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result

    result = await service.get_accessible_projects(mock_db, make_user())

    assert result == []