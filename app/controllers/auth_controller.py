from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas.schemas import UserCreate, UserLogin, Token
from ..services.auth_service import AuthService, get_db

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    creating a new user and return access token
    """
    service = AuthService(db)
    
    # to check if user exists
    if service.repository.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # toreate user and return token
    db_user = service.create_user(user.email, user.password)
    return service.authenticate_user(user.email, user.password)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticating user and return access token
    """
    service = AuthService(db)
    result = service.authenticate_user(user.email, user.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return result
