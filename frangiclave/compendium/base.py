from contextlib import contextmanager
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///frangiclave.db')
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base = declarative_base()


class GameContentMixin:
    @classmethod
    def from_data(cls, file_name: 'File', data: Dict[str, Any]):
        raise NotImplementedError
