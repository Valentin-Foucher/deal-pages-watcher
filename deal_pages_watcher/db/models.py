from datetime import datetime

from sqlalchemy import Column, String, Date, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from deal_pages_watcher.db.core import Model


class User(Model):
    __tablename__ = 'users'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False)
    password = Column('password', String, nullable=False)
    watcher: Mapped['Watcher'] = relationship(back_populates='user', cascade='all, delete-orphan')


class Watcher(Model):
    __tablename__ = 'watchers'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    url = Column('url', String, nullable=False)
    alert_sent = Column('alert_sent', Boolean, default=False)
    product = Column('product', String)
    creation_date = Column('creation_date', Date, default=datetime.utcnow)

    user_id = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='watcher')

