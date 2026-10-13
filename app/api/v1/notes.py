from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.crud import note as note_crud
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.note import NoteCreate, NotePage, NoteRead, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=NotePage)
def list_notes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    items, total = note_crud.list_paginated(
        db, page=page, size=size, public_only=True, search=search
    )
    return NotePage(items=items, total=total, page=page, size=size)

@router.post("", response_model=NoteRead, status_code=201)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    return note_crud.create(db, author_id=current.id, data=data)

@router.get("/{note_id}", response_model=NoteRead)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    note = note_crud.get(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    if not note.is_public and note.author_id != current.id and current.role != UserRole.ADMIN:
        raise HTTPException(403, "Access denied")
    return note

@router.patch("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    note = note_crud.get(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    if note.author_id != current.id and current.role not in (UserRole.MODERATOR, UserRole.ADMIN):
        raise HTTPException(403, "Access denied")
    return note_crud.update(db, note, data)

@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    note = note_crud.get(db, note_id)
    if not note:
        raise HTTPException(404, "Note not found")
    if note.author_id != current.id and current.role != UserRole.ADMIN:
        raise HTTPException(403, "Access denied")
    note_crud.delete(db, note)