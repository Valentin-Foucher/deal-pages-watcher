from typing import Any

from frozendict import frozendict


def wrap(obj: Any) -> list[Any]:
    return obj if isinstance(obj, list) else [obj]


def get_nested_element(d: dict[str, Any], path: str) -> Any:
    v = d
    for p in path.split('.'):
        if p not in v:
            return None
        v = v.get(p)

    if isinstance(v, dict):
        v = frozendict(v)
    elif isinstance(v, list):
        v = tuple(v)

    return v
