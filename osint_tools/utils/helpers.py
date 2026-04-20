"""General-purpose helper utilities."""

import json
import re
from typing import Any, Callable, Iterable, List


def validate_url(url: str) -> bool:
    """Validate whether a string is a well-formed URL.

    Args:
        url: The string to validate.

    Returns:
        ``True`` if the URL looks valid, ``False`` otherwise.
    """
    regex = re.compile(r"^(https?://)([a-z0-9-]+\.)+[a-z]{2,}(/.*)?$", re.IGNORECASE)
    return bool(re.match(regex, url))


def format_json(data: Any, indent: int = 4) -> str:
    """Serialise *data* as a pretty-printed JSON string.

    Args:
        data: Any JSON-serialisable Python object.
        indent: Number of spaces used for indentation.

    Returns:
        A formatted JSON string.
    """
    return json.dumps(data, indent=indent, default=str)


def batch_process(
    items: Iterable[Any],
    function: Callable,
    *args: Any,
    **kwargs: Any,
) -> List[Any]:
    """Apply *function* to every item in *items*.

    Args:
        items: An iterable of inputs.
        function: A callable that accepts an item as its first argument.
        *args: Extra positional arguments forwarded to *function*.
        **kwargs: Extra keyword arguments forwarded to *function*.

    Returns:
        A list of results in the same order as *items*.
    """
    return [function(item, *args, **kwargs) for item in items]
