from deal_pages_watcher.api_clients.alerts.interface import Client


class TelegramClient(Client):
    def send(self, text: str):
        self._post(f'bot{self._config["token"]}/sendMessage', {},
                   query_parameters=dict(chat_id=self._config['channel'], text=text),
                   status_code=200)

