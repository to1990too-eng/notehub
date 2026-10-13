from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.crud import note as note_crud
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.note import NotePage
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def me(current: User = Depends(get_current_user)):
    return current

@router.get("/me/notes", response_model=NotePage)
def my_notes(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    items, total = note_crud.list_paginated(
        db, page=page, size=size, author_id=current.id
    )
    return NotePage(items=items, total=total, page=page, size=size)

@router.get("/{user_id}/notes", response_model=NotePage)
def user_public_notes(
    user_id: int,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
):
    items, total = note_crud.list_paginated(
        db, page=page, size=size, author_id=user_id, public_only=True
    )
    return NotePage(items=items, total=total, page=page, size=size)