import pytest
from app.models import Category

def test_create_category(test_db):
    category = Category(name="Test Category", description="Test Description")
    test_db.add(category)
    test_db.commit()
    
    db_category = test_db.query(Category).first()
    assert db_category.name == "Test Category"
    assert db_category.description == "Test Description"

def test_unique_category_name(test_db):
    category1 = Category(name="Test Category")
    category2 = Category(name="Test Category")
    
    test_db.add(category1)
    test_db.commit()
    
    with pytest.raises(Exception):
        test_db.add(category2)
        test_db.commit()