from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse
from crud.user import create_user, get_user_by_email
from core.auth import verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists — can't have duplicates
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db, user)


@router.post("/login")
def login(
    # OAuth2PasswordRequestForm expects "username" + "password" as form fields
    # We use username field to hold the email — OAuth2 standard requires this name
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)

    # Two checks in one line — user exists AND password matches
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Store email in token as "sub" — JWT standard field name for subject
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}