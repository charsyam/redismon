from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

engine = None
db_session = None
Base = None

def init_db(database_uri):
    print(database_uri)

    global engine
    global db_session
    global Base

    engine = create_engine(database_uri)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    print(engine)
    print(db_session)
    Base = declarative_base()
    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)

    return db_session
