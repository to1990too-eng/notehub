from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def create(db: Session, author_id: int, data: NoteCreate) -> Note:
    note = Note(author_id=author_id, **data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get(db: Session, note_id: int) -> Note | None:
    return db.get(Note, note_id)

def list_paginated(
    db: Session,
    *,
    page: int,
    size: int,
    author_id: int | None = None,
    public_only: bool = False,
    search: str | None = None,
) -> tuple[list[Note], int]:
    stmt = select(Note)
    if author_id is not None:
        stmt = stmt.where(Note.author_id == author_id)
    if public_only:
        stmt = stmt.where(Note.is_public.is_(True))
    if search:
        stmt = stmt.where(Note.title.ilike(f"%{search}%"))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(Note.created_at.desc()).offset((page - 1) * size).limit(size)
    ).all()
    return list(items), total

def update(db: Session, note: Note, data: NoteUpdate) -> Note:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note

def delete(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()