from typing import Dict, Any, Callable, Union


def to_bool(val: Union[bool, str]) -> bool:
    if isinstance(val, bool):
        return val
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
