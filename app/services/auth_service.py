from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from ..config import get_settings
from ..repositories.auth_repository import AuthRepository
from ..models.models import Base

# Database setup
settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)
        self.settings = get_settings()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, user_id: int) -> str:
        expires_delta = timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(
            to_encode, 
            self.settings.SECRET_KEY, 
            algorithm=self.settings.ALGORITHM
        )

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        user = self.repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
            
        token = self.create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    def create_user(self, email: str, password: str):
        hashed_password = self.get_password_hash(password)
        db_user = self.repository.create_user(email, hashed_password)
        return db_user
