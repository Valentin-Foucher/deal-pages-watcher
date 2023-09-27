from abc import ABC, abstractmethod

from deal_pages_watcher.api_clients.base import BaseJsonRestClient


class Client(BaseJsonRestClient, ABC):
    @abstractmethod
    def send(self, text: str) -> None:
        raise NotImplementedError
