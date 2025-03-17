import pytest
from app.models import Tag

def test_create_tag(db_session):
    tag = Tag(name="TestTag")
    test_db.add(tag)
    test_db.commit()
    
    db_tag = test_db.query(Tag).first()
    assert db_tag.name == "TestTag"

def test_unique_tag_name(db_session):
    tag1 = Tag(name="TestTag")
    tag2 = Tag(name="TestTag")
    
    test_db.add(tag1)
    test_db.commit()
    
    with pytest.raises(Exception):
        test_db.add(tag2)
        test_db.commit()