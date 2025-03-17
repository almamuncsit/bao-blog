import pytest
from app.models import Category

def test_create_category(db_session):
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    db_category = db_session.query(Category).first()
    assert db_category.name == "Test Category"
    assert db_category.description == "Test Description"

def test_unique_category_name(db_session):
    category1 = Category(name="Test Category")
    category2 = Category(name="Test Category")
    
    db_session.add(category1)
    db_session.commit()
    
    with pytest.raises(Exception):
        db_session.add(category2)
        db_session.commit()