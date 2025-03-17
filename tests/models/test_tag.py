import pytest
from app.models import Tag

def test_create_tag(db_session):
    tag = Tag(name="TestTag")
    db_session.add(tag)
    db_session.commit()
    
    db_tag = db_session.query(Tag).first()
    assert db_tag.name == "TestTag"

def test_unique_tag_name(db_session):
    tag1 = Tag(name="TestTag")
    tag2 = Tag(name="TestTag")
    
    db_session.add(tag1)
    db_session.commit()
    
    with pytest.raises(Exception):
        db_session.add(tag2)
        db_session.commit()