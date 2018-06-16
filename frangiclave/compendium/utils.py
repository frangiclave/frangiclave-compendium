from typing import Dict, List, Any, Callable


def to_bool(val: str) -> bool:
    return val == 'true'


def to_int_dict(val: Dict[str, str]) -> Dict[str, int]:
    return {k: int(v) for k, v in val.items()}


def get(
        data: Dict[str, Any],
        key: str,
        default: Any = None,
        conversion_function: Callable = None
) -> Any:
    if key in data:
        if conversion_function:
            return conversion_function(data[key])
        return data[key]
    return default
