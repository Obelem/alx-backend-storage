#!/usr/bin/env python3
''' write strings to Redis '''
import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """decorator for counting calls

    Args:
        method (Callable): _description_

    Returns:
        Callable: _description_
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper decorator

        Returns:
            _type_: _description_
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """redis basics"""

    def __init__(self):
        """init redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid),
        store the input data in Redis using the random
        key and return the key.

        Args:
            data (Union[str, bytes, int, float]): _description_

        Returns:
            str: random key generated
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """_summary_

        Args:
            key (str): _description_
            fn (Optional[Callable], optional): _description_. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: _description_
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Parameterizes a value from redis to str using utf-8 charset

        Args:
            key (str): _description_

        Returns:
            str: _description_
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Parameterizes a value from redis to int

        Args:
            key (str): _description_

        Returns:
            int: _description_
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
