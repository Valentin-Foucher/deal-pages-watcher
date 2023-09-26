from datetime import datetime

from sqlalchemy import Column, String, Date, Integer

from deal_pages_watcher.db.core import Model


class Watcher(Model):
    __tablename__ = 'watchers'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    owner = Column('owner', String)
    url = Column('x', String)
    creation_date = Column('creation_date', Date, default=datetime.utcnow)
