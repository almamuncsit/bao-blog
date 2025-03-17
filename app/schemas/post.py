from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None


class PostCreate(PostBase):
    tag_ids: Optional[List[int]] = None


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)