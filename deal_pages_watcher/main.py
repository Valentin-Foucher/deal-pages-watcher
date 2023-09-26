from deal_pages_watcher.db.core import init_db
from deal_pages_watcher.db.query import list_watchers

init_db()

for watcher in list_watchers('a'):
    print(watcher)
