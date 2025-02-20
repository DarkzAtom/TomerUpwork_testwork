from sqlalchemy.orm import Session
from ..models.models import User
from typing import Optional

class AuthRepository:
    """
    Repository for handling all user-related database operations
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, hashed_password: str) -> User:
        db_user = User(email=email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
