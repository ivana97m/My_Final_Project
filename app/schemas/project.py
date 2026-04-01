from pydantic import BaseModel, Field
from datetime import datetime

class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1, max_length=20)

class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1, max_length=20)

class ProjectInfoResponse(BaseModel):
    id: int
    name: str
    description: str | None
    total_size_bytes: int
    created_at: datetime
    updated_at: datetime

class ProjectFullResponse(ProjectInfoResponse):
    documents: list[DocumentResponse] = []

    model_config = {"from_attributes": True}
