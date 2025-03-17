from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, Tag as TagSchema

router = APIRouter()


@router.post("/", response_model=TagSchema)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    try:
        db_tag = Tag(name=tag.name)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tag with this name already exists"
        )


@router.get("/", response_model=List[TagSchema])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags


@router.get("/{tag_id}", response_model=TagSchema)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put("/{tag_id}", response_model=TagSchema)
def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db_tag.name = tag.name
    try:
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tag with this name already exists"
        )


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
