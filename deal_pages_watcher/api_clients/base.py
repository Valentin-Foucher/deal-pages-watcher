from typing import Any, Callable, Union, Optional, IO

import requests

from deal_pages_watcher import config
from deal_pages_watcher.constants import BASE_CLIENT_TYPE
from deal_pages_watcher.utils.object_utils import get_nested_element, wrap


class BaseJsonRestClient:
    def __init__(self, config_: dict[str, Union[str, int]]):
        self._config = config_

    def _request(
            self,
            method: Callable[..., requests.Response],
            path: str,
            client_type: str = BASE_CLIENT_TYPE,
            status_code: Optional[int] = None,
            **kwargs
    ) -> requests.Response:
        tries_count = 0
        expected_status_codes = wrap(status_code)

        url = f'{get_nested_element(self._config, f"urls.{client_type}")}/{path}'
        while True:
            response = method(url, **kwargs)
            if tries_count < config.get('http_client.max_retries') \
                    or (not status_code or response.status_code in expected_status_codes):
                break

            tries_count += 1

        if status_code and response.status_code not in expected_status_codes:
            raise RuntimeError(f'Unexpected status code ({response.status_code}): {response.text}')

        return response

    def _get(
            self,
            path: str,
            *,
            headers: Optional[dict[str, str]] = None,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[Union[int, list[int]]] = None,
            **kwargs
    ) -> requests.Response:
        return self._request(requests.get, path,
                             headers=headers,
                             params=query_parameters,
                             status_code=status_code,
                             **kwargs)

    def _put(
            self,
            path: str,
            data: dict[Any, Any],
            *,
            headers: Optional[dict[str, str]] = None,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[Union[int, list[int]]] = None,
            **kwargs
    ) -> requests.Response:
        return self._request(requests.put, path,
                             data=data,
                             headers=headers,
                             params=query_parameters,
                             status_code=status_code,
                             **kwargs)

    def _post(
            self,
            path: str,
            data: dict[Any, Any],
            *,
            files: Optional[dict[str, IO]] = None,
            headers: Optional[dict[str, str]] = None,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[Union[int, list[int]]] = None,
            **kwargs
    ) -> requests.Response:
        return self._request(requests.post, path,
                             data=data,
                             files=files,
                             headers=headers,
                             params=query_parameters,
                             status_code=status_code,
                             **kwargs)

    def _delete(
            self,
            path: str,
            *,
            headers: Optional[dict[str, str]] = None,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[Union[int, list[int]]] = None,
            **kwargs
    ) -> requests.Response:
        return self._request(requests.get, path,
                             headers=headers,
                             params=query_parameters,
                             status_code=status_code,
                             **kwargs)
