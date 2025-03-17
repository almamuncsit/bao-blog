import pytest
from datetime import datetime
from app.models import Post, Category, Tag

def test_create_post(test_db):
    post = Post(
        title="Test Post",
        content="Test Content"
    )
    test_db.add(post)
    test_db.commit()
    
    db_post = test_db.query(Post).first()
    assert db_post.title == "Test Post"
    assert db_post.content == "Test Content"
    assert isinstance(db_post.created_at, datetime)
    assert isinstance(db_post.updated_at, datetime)

def test_post_with_category(test_db):
    category = Category(name="Test Category")
    test_db.add(category)
    test_db.commit()
    
    post = Post(
        title="Test Post",
        content="Test Content",
        category_id=category.id
    )
    test_db.add(post)
    test_db.commit()
    
    db_post = test_db.query(Post).first()
    assert db_post.category.name == "Test Category"

def test_post_with_tags(test_db):
    tag1 = Tag(name="Tag1")
    tag2 = Tag(name="Tag2")
    test_db.add_all([tag1, tag2])
    test_db.commit()
    
    post = Post(
        title="Test Post",
        content="Test Content",
        tags=[tag1, tag2]
    )
    test_db.add(post)
    test_db.commit()
    
    db_post = test_db.query(Post).first()
    assert len(db_post.tags) == 2
    assert {tag.name for tag in db_post.tags} == {"Tag1", "Tag2"}