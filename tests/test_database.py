import pytest
from sqlalchemy.orm import Session
from app.database import get_db

def test_get_db():
    db = next(get_db())
    assert isinstance(db, Session)
    db.close()