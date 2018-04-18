from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config import config


def __construct_engine_url(dialect: str, driver: Optional[str], username: Optional[str], password: Optional[str],
                           host: Optional[str], port: Optional[str], database: Optional[str]) -> str:
    """dialect+driver://username:password@host:port/database"""
    result = dialect
    if driver:
        result = f'{result}+{driver}'
    result = f'{result}://'
    if username and password:
        result = f'{result}{username}:{password}@'
    if host:
        result = f'{result}{host}'
        if port:
            result = f'{result}:{port}'
    if database:
        result = f'{result}/{database}'
    return result


def __db_cfg(key: str):
    return config['DB'][key] if key in config['DB'] else None


__engine_url = __construct_engine_url(dialect=__db_cfg('DIALECT'), driver=__db_cfg('DRIVER'),
                                      username=__db_cfg('USERNAME'), password=__db_cfg('PASSWORD'),
                                      host=__db_cfg('HOST'), port=__db_cfg('PORT'),
                                      database=__db_cfg('DATABASE'))

# Import metadata, engine for creating tables (app startup)
metadata = MetaData()
db_engine = create_engine(__engine_url)

__session_factory = sessionmaker(bind=db_engine)

# Import Base for defining tables (pre-app startup)
Base = declarative_base(metadata=metadata)

# Import Session to create SQLAlchemy Sessions for database interactions. Can't be passed among threads. (runtime)
# http://docs.sqlalchemy.org/en/latest/orm/contextual.html
Session = scoped_session(__session_factory)


# Basic session scope. Use as `with session_scope() as session: ...`
# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def db_session(func):
    """Decorator to pass a `session` into decorated function"""

    def decorated_function(*args, **kwargs):
        with session_scope() as session:
            return func(*args, **kwargs, session=session)

    return decorated_function
