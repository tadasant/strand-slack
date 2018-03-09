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


def db_cfg(key: str):
    return config['DB'][key] if key in config['DB'] else None


__engine_url = __construct_engine_url(dialect=db_cfg('DIALECT'), driver=db_cfg('DRIVER'),
                                      username=db_cfg('USERNAME'), password=db_cfg('PASSWORD'),
                                      host=db_cfg('HOST'), port=db_cfg('PORT'),
                                      database=db_cfg('DATABASE'))

# Import metadata, engine for creating tables (app startup)
metadata = MetaData()
engine = create_engine(__engine_url)

__session_factory = sessionmaker(bind=engine)

# Import Base for defining tables (pre-app startup)
Base = declarative_base(metadata=metadata)

# Import Session to create SQLAlchemy Sessions for database interactions. Can't be passed among threads. (runtime)
# http://docs.sqlalchemy.org/en/latest/orm/contextual.html
Session = scoped_session(__session_factory)
