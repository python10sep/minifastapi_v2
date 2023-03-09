"""
Install SQLITE DB
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./tracker.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TODO
# Refer - https://docs.sqlalchemy.org/en/14/orm/session_basics.html#when-do-i-make-a-sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


