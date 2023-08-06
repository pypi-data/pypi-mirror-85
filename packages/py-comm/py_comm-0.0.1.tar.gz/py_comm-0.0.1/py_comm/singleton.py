# -*- coding: utf-8 -*-

from threading import Lock


class Singleton(type):
    """
    Thread-safe singleton pattern, using double-checked locking.
    Examples:
        >>> class Foo(metaclass=Singleton):
        ...     def __init__(self, name):
        ...         self.name = name
        >>> a = Foo("a")
        >>> b = Foo("b")
        >>> assert a is b
        >>> assert b.name == "a"
    """

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
