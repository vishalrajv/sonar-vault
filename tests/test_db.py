import pytest
from sqlalchemy.orm import Session
from database.db import get_db, SessionLocal, engine
from models.base import Base

def test_get_db():
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)
    db.close()

def test_base_metadata():
    assert Base.metadata is not None
