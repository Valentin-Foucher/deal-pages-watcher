from sqlalchemy import select, ScalarResult

from deal_pages_watcher.db.core import session
from deal_pages_watcher.db.models import Watcher, User


def list_watchers(name: str) -> ScalarResult[Watcher]:
    return session.scalars(
        select(Watcher)
        .join(Watcher.user)
        .where(User.name == name)
    )
