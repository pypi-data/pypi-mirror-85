"""
Database functionality.
"""

import sqlalchemy
import logging
import inspect
from contextlib import contextmanager

@contextmanager
def scoped_session(sessionmaker):
    """
    Provide a transactional scope around a series of operations.
    Can also be used as a decorator.

    Usage:
    with session as session_scope(session_maker):
        ...
    """
    session = sessionmaker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class DBWrapper():
    """
    A generic DB wrapper class to add and retrieve (with filtering) its data,
    hiding the details over the sessions.
    """

    def __init__(self, sessionmaker):
        """
        Initialize the dbw class using an engine.
        """
        self.sessionmaker = sessionmaker

    def add(self, Item, **kwargs):

        if inspect.isclass(Item):
            new_item = Item(**kwargs)
        else:
            new_item = Item

        with scoped_session(self.sessionmaker) as session:
            session.add(new_item)

    def retrieve(self, Item, **kwargs):
        with scoped_session(self.sessionmaker) as session:
            query = session.query(Item)
            for key, value in kwargs.items():
                query = query.filter(getattr(Item, key) == value)
        return query
