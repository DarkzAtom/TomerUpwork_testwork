from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas.schemas import PostCreate, Post, PostList
from ..services.post_service import PostService
from ..services.auth_service import get_db
from ..dependencies.auth import get_current_user
from ..models.models import User

router = APIRouter()

@router.post("/posts", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creating a new post for the authenticated user
    """
    service = PostService(db)
    return service.create_post(current_user.id, post.text)

@router.get("/posts", response_model=PostList)
async def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    get all posts for the authenticated user
    """
    service = PostService(db)
    posts = service.get_user_posts(current_user.id)
    return {"posts": posts}

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a post
    """
    service = PostService(db)
    if not service.delete_post(post_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not owned by user"
        )
