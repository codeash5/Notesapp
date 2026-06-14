from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.config import settings
from db.database import get_db

# The hashing machine — configured to use bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI: "tokens come from /auth/login"
# This is what makes the Authorize button appear in Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    # Converts "hello123" → "$2b$12$XYZ..." irreversibly
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Hashes plain_password and checks if it matches stored hash
    # Returns True (let in) or False (reject)
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Set expiry time — token dies after 30 minutes
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Bake the expiry into the token payload
    to_encode.update({"exp": expire})
    # Sign and encode the token using your SECRET_KEY
    # Only your server can create valid tokens because only you know the key
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),  # extracts token from Authorization header
    db: Session = Depends(get_db)         # gives us a database session
):
    # This error is ready to raise if anything goes wrong
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token — verifies signature + expiry automatically
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # Extract email from payload — we stored it as "sub" at login
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # Token tampered with, expired, or invalid — reject
        raise credentials_exception

    # Import here to avoid circular imports between modules
    from crud.user import get_user_by_email
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    # Return the actual User ORM object — routes receive this
    return user