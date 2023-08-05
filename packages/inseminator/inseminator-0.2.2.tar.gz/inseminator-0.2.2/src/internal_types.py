from typing import Callable, TypeVar, Union, Any

T = TypeVar("T")
Dependable = Union[Callable[..., T], Any]
