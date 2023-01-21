import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv(find_dotenv())

MYSQL_URI = os.getenv("MYSQL_URI")

meta = MetaData()

engine = create_engine(MYSQL_URI)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initializes database using SQLAlchemy session"""
    import models
    Base.metadata.create_all(bind=engine)
