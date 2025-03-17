from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import PostCreate, Post as PostSchema

router = APIRouter()


@router.post("/", response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        db_post = Post(
            title=post.title,
            content=post.content,
            category_id=post.category_id
        )
        if post.tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
            if len(tags) != len(post.tag_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more tag IDs are invalid"
                )
            db_post.tags = tags
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category ID"
        ) from exc


@router.get("/", response_model=List[PostSchema])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=PostSchema)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    try:
        db_post.title = post.title
        db_post.content = post.content
        db_post.category_id = post.category_id
        
        if post.tag_ids is not None:
            tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
            if len(tags) != len(post.tag_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more tag IDs are invalid"
                )
            db_post.tags = tags
        
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category ID"
        ) from exc


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}