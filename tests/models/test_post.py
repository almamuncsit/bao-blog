import pytest
from datetime import datetime
from app.models import Post, Category, Tag

def test_create_post(db_session):
    post = Post(
        title="Test Post",
        content="Test Content"
    )
    db_session.add(post)
    db_session.commit()
    
    db_post = db_session.query(Post).first()
    assert db_post.title == "Test Post"
    assert db_post.content == "Test Content"
    assert isinstance(db_post.created_at, datetime)
    assert isinstance(db_post.updated_at, datetime)

def test_post_with_category(db_session):
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    
    post = Post(
        title="Test Post",
        content="Test Content",
        category_id=category.id
    )
    db_session.add(post)
    db_session.commit()
    
    db_post = db_session.query(Post).first()
    assert db_post.category.name == "Test Category"

def test_post_with_tags(db_session):
    tag1 = Tag(name="Tag1")
    tag2 = Tag(name="Tag2")
    db_session.add_all([tag1, tag2])
    db_session.commit()
    
    post = Post(
        title="Test Post",
        content="Test Content",
        tags=[tag1, tag2]
    )
    db_session.add(post)
    db_session.commit()
    
    db_post = db_session.query(Post).first()
    assert len(db_post.tags) == 2
    assert {tag.name for tag in db_post.tags} == {"Tag1", "Tag2"}