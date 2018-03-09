from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


__cfg = config['DB']
__engine_url: str = __construct_engine_url(dialect=__cfg['DIALECT'], driver=__cfg['DRIVER'], username=__cfg['USERNAME'],
                                           password=__cfg['PASSWORD'], host=__cfg['HOST'], port=__cfg['PORT'],
                                           database=__cfg['DATABASE'])
__database_engine = create_engine(__engine_url)

# Import Session to create SQLAlchemy Sessions for database interactions
Session = sessionmaker(bind=__database_engine)
