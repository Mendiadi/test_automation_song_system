import string
import secrets
import inspect
import functools
import socket
from typing import Callable


def expected_msg(msg) -> Callable[[str], str]:
    """Return a function that build msg with args"""
    return functools.partial(lambda user, string: string % user,
                             string=msg)


def my_origin(call=3):
    """Get the file::function name
    using inspect to get the last call in the stack before this
    call executed."""
    origin = inspect.stack()[call]
    filename = origin.filename.split("\\")[-1]
    return f"{filename}::def {origin.function}(...)::line {origin.lineno}"


def build_str(func, range_, *args, space=False) -> str:
    r = ""
    for _ in range(range_):
        r += func(*args)
        if space: r += " "
    return r


def random_name(length: int = 6) -> str:
    """Get random name"""
    return build_str(secrets.choice, length, string.ascii_lowercase).capitalize()


def random_pass(length=8) -> str:
    """Get random password"""
    all__ = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return build_str(secrets.choice, length, all__)


def random_title(words=3) -> str:
    """Get random title"""
    lens = (3, 4, 5, 6)
    return build_str(random_name, words, secrets.choice(lens), space=True)


def random_year() -> int:
    """Get random year"""
    return secrets.choice(range(1900, 2023))


def get_generic_random_schema(attributes: list[tuple[str, type]],
                              manual_attributes: dict,
                              cls: type) -> object:
    """Generic parse and return random schema"""
    schema = {}
    for attr, type_ in attributes:
        if "password" in attr:
            schema[attr] = random_pass()
        elif "name" in attr:
            schema[attr] = random_name()
        elif "title" in attr:
            schema[attr] = random_title()
        elif "year" in attr:
            schema[attr] = random_year()
        else:
            schema[attr] = random_name()
    schema.update(manual_attributes)
    return cls(**schema)
