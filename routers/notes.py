from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.note import NoteCreate, NoteUpdate, NoteResponse
from crud.note import get_user_notes, get_note, create_note, update_note, delete_note
from core.auth import get_current_user
from models.user import User
from typing import List

router = APIRouter()


@router.get("/", response_model=List[NoteResponse])
def read_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # protected
):
    return get_user_notes(db, current_user.id)


@router.post("/", response_model=NoteResponse, status_code=201)
def create_new_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # protected
):
    return create_note(db, note, current_user.id)


@router.put("/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = update_note(db, note_id, note, current_user.id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return updated


@router.delete("/{note_id}", status_code=204)
def delete_existing_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_note(db, note_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )