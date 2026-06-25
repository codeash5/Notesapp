from sqlalchemy.orm import Session
from models.note import Note
from schemas.note import NoteCreate, NoteUpdate


def get_user_notes(db: Session, user_id: int, limit: int = 10, offset: int = 0):
    return (
        db.query(Note)
        .filter(Note.owner_id == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_note(db: Session, note_id: int, user_id: int):
    # Get specific note — must belong to this user
    return db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user_id
    ).first()


def create_note(db: Session, note: NoteCreate, user_id: int):
    # owner_id comes from the logged-in user — not from request body
    db_note = Note(**note.model_dump(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, note: NoteUpdate, user_id: int):
    db_note = get_note(db, note_id, user_id)
    if not db_note:
        return None
    # Only update fields that were actually sent
    update_data = note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int, user_id: int):
    db_note = get_note(db, note_id, user_id)
    if not db_note:
        return None
    db.delete(db_note)
    db.commit()
    return db_note