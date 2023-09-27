from deal_pages_watcher import config
from deal_pages_watcher.api_clients.alerts.telegram import TelegramClient
from deal_pages_watcher.db.core import init_db, session
from deal_pages_watcher.db.query import list_watchers
from deal_pages_watcher.scrapping.deals import get_discount_details

init_db()
telegram_client = TelegramClient(config.get('telegram'))

new_deals = ''
finished_deals = ''
message = ''

for watcher in list_watchers('valentin'):
    details = get_discount_details(watcher.url)

    if details['discount'] and not watcher.alert_sent:
        new_deals += f'- {details["product"]}: ' \
                     f'{details["prices"][1]["value"]}{details["prices"][1]["currency"]} -> ' \
                     f'{details["prices"][0]["value"]}{details["prices"][0]["currency"]} ' \
                     f'({int(details["discount"])}%)\n'

        watcher.alert_sent = True
        watcher.product = details['product']
        session.commit()
    elif not details['discount'] and watcher.alert_sent:
        finished_deals += f'- {details["product"]}\n'
        watcher.alert_sent = False
        watcher.product = None
        session.commit()

if new_deals:
    message = f'Deals found for following products:\n{new_deals}'
    if finished_deals:
        message += '\n\n'
if finished_deals:
    message += f'Finished deals for following products: {finished_deals}'

if message:
    telegram_client.send(message)
