from sqlalchemy.orm import Session
from ..models.models import Post
from typing import List, Optional

class PostRepository:
    """
    Repository for handling all post-related database operations
    """
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user_id: int, text: str) -> Post:
        
        db_post = Post(text=text, user_id=user_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def get_user_posts(self, user_id: int) -> List[Post]:
        
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def delete_post(self, post_id: int, user_id: int) -> bool:
        
        post = self.db.query(Post).filter(
            Post.id == post_id,
            Post.user_id == user_id
        ).first()
        
        if post:
            self.db.delete(post)
            self.db.commit()
            return True
        return False
