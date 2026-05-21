from sqlalchemy.orm import Session

from ..models.user import User
from ..core.security import hash_password, verify_password


def get_user_by_username(db: Session, username: str):
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, password: str) -> User:
    """Create a new user with hashed password."""
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user_password(db: Session, username: str, password: str):
    """Verify user credentials."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
