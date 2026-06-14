from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.auth import hash_password


def get_user_by_email(db: Session, email: str):
    # SELECT * FROM users WHERE email = ? LIMIT 1
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    # Hash the password BEFORE touching the database
    hashed = hash_password(user.password)

    # Create ORM object — not in DB yet, just in Python memory
    db_user = User(email=user.email, hashed_password=hashed)

    # Tell the session "track this object"
    db.add(db_user)

    # Actually write to PostgreSQL
    db.commit()

    # Refresh so db_user now includes the id PostgreSQL generated
    db.refresh(db_user)

    return db_user