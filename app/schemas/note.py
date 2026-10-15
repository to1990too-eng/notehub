from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    is_public: bool = True


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    is_public: bool | None = None


class NoteRead(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class NotePage(BaseModel):
    items: list[NoteRead]
    total: int
    page: int
    size: int
