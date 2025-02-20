from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
import functools
import time

from ..repositories.post_repository import PostRepository
from ..models.models import Post
from ..config import get_settings

class PostService:
    def __init__(self, db: Session):
        self.repository = PostRepository(db)
        self.settings = get_settings()
        self._cache = {}

    def create_post(self, user_id: int, text: str) -> Post:
        self._invalidate_cache(user_id)
        return self.repository.create_post(user_id, text)

    @functools.lru_cache(maxsize=1000)
    def get_user_posts(self, user_id: int) -> List[Post]:
        cache_key = f"user_posts_{user_id}"
        
        # Check cache
        cached_data = self._cache.get(cache_key)
        if cached_data:
            posts, timestamp = cached_data
            if time.time() - timestamp < (self.settings.CACHE_EXPIRE_MINUTES * 60):
                return posts

        # Get fresh data
        posts = self.repository.get_user_posts(user_id)
        self._cache[cache_key] = (posts, time.time())
        return posts

    def delete_post(self, post_id: int, user_id: int) -> bool:
        self._invalidate_cache(user_id)
        return self.repository.delete_post(post_id, user_id)

    def _invalidate_cache(self, user_id: int):
        cache_key = f"user_posts_{user_id}"
        self._cache.pop(cache_key, None) 