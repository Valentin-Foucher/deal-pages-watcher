from typing import Any

from pyaml_env import parse_config

from deal_pages_watcher.utils.object_utils import get_nested_element


def load_config(config_file: str = 'config.yaml') -> dict[str, Any]:
    return parse_config(config_file)


def get(path: str) -> Any:
    return get_nested_element(_config, path)


_config = load_config()
