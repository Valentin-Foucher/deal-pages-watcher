from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from deal_pages_watcher import config

engine = create_engine(config.get('postgres.connection_string'))

session = scoped_session(sessionmaker(bind=engine))

Model = declarative_base(name='Model')
Model.query = session.query_property()


def init_db():
    Model.metadata.create_all(bind=engine)
