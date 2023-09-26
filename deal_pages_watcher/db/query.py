from sqlalchemy import select, ScalarResult

from deal_pages_watcher.db.core import session
from deal_pages_watcher.db.models import Watcher


def list_watchers(owner: str) -> ScalarResult[Watcher]:

    return session.scalars(
        select(Watcher).where(Watcher.owner == owner)
    )
