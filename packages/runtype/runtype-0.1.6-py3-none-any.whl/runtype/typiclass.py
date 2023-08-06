from copy import copy
from dataclasses import dataclass as _dataclass



def __post_init__(self, isinstance=isa):
    for name, field in getattr(self, '__dataclass_fields__', {}).items():
        value = getattr(self, name)
        if not isinstance(value, field.type):
            raise TypeError(f"[{type(self).__name__}] Attribute '{name}' expected value of type {field.type}, instead got {value!r}")

def remake(self, **kwargs):
    """Returns a new instance, with the given attibutes overwriting the existing ones.

    Useful for making copies with small updates.

    Examples:
        >>> @dataclass
        ... class A:
        ...     a: int
        ...     b: int
        >>> A(1, 2).remake(a=-2)
        A(a=-2, b=2)

        >>> some_instance.remake() == copy(some_instance)   # Equivalent operations
        True
    """
    attrs = dict(self)
    attrs.update(kwargs)
    return type(self)(**attrs)

def __iter__(self):
    "Yields a list of tuples [(name, value), ...]"
    return ((name, getattr(self, name)) for name in self.__dataclass_fields__)

def values(self):
    """Returns a list of values

    Equivalent to: list(dict(this).values())
    """
    return [getattr(self, name) for name in self.__dataclass_fields__]


def _set_if_not_exists(cls, d):
    for attr, value in d.items():
        try:
            getattr(cls, attr)
        except AttributeError:
            setattr(cls, attr, value)

def dataclass(cls, frozen=True, isinstance=isa):
    """typical.dataclass adds functionality on top of Python's built-in dataclass.

    * Adds run-time type verification
    * Adds convenience methods:

        * remake - create a new instance, with updated attributes
        * values - returns the dataclass values as a list
        * dict(this) - returns a dict of the dataclass attributes and values

    NOTE: Due to a technical issue, typical ignores all user-defined __post_init__() methods.
          Instead, users can define the __created__() method, that will be called
          after initialization and verification are done.

    Example:
        >>> @dataclass
        >>> class Point:
        ...     x: int
        ...     y: int

        >>> p = Point(2, 3)
        >>> p
        Point(x=2, y=3)
        >>> dict(p)         # Maintains order
        {'x': 2, 'y': 3}

        >>> p.remake(x=30)  # New instance
        Point(x=30, y=3)
    """
    orig_post_init = getattr(cls, '__post_init__', None)
    def __post_init(self):
        __post_init__(self, isinstance=isinstance)
        if orig_post_init is not None:
            orig_post_init(self)
    c = copy(cls)
    c.__post_init__ = __post_init
    _set_if_not_exists(c, {
        'remake': remake,
        'values': values,
        '__iter__': __iter__,
    })
    return _dataclass(c, frozen=frozen)

