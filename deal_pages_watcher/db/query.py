from sqlalchemy import select, ScalarResult

from deal_pages_watcher.db.core import session
from deal_pages_watcher.db.models import Watcher, User


def list_watchers() -> ScalarResult[Watcher]:
    return session.scalars(
        select(Watcher)
        .join(Watcher.user)
    )


def create_watcher(url: str):
    session.add(Watcher(url=url, user_id=1))
    session.commit()


def delete_watcher(watcher: Watcher):
    session.delete(watcher)
    session.commit()


def get_watcher(url: str) -> Watcher:
    return session.query(Watcher).filter_by(url=url).first()

