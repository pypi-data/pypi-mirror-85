import inspect
from typing import Any, Callable, Dict, Optional, Protocol, Type, TypeVar, Union, cast, get_type_hints

from .dependency import Dependency, StaticDependency
from .exceptions import ResolverError
from .scoped_dict import ScopedDict

T = TypeVar("T")

Dependable = Union[Callable[..., T], Type[T]]


class DependencyResolver:
    def __init__(self, container: ScopedDict[Dependable, Dependency]) -> None:
        self._container = container

    def resolve(self, dependency: Dependable, parameters: Optional[Dict[str, Any]] = None) -> Dependency[T]:
        if dependency in self._container:
            return self._container[dependency]

        callable_dependency: Callable
        if inspect.isclass(dependency):
            if issubclass(cast(type, dependency), cast(type, Protocol)):
                raise ResolverError(f"Implementation for {dependency.__name__} protocol is not defined.")

            callable_dependency = dependency.__init__  # type: ignore
        elif inspect.isfunction(dependency):
            callable_dependency = dependency

        type_hints = get_type_hints(callable_dependency)
        args: Dict[str, Any] = {}

        if parameters:
            parameter_names = type_hints.keys()

            for parameter_name, parameter_value in parameters.items():
                if parameter_name not in parameter_names:
                    raise ResolverError(f"Parameter {parameter_name} it not part of {dependency.__name__}'s signature.")

                args[parameter_name] = parameter_value

        signature_parameters = inspect.signature(callable_dependency).parameters
        for parameter_name, parameter_dependency in type_hints.items():
            if parameter_name == "return" or parameter_name in args:
                continue

            if (default_value := signature_parameters[parameter_name].default) != inspect.Signature.empty:
                args[parameter_name] = default_value
            else:
                args[parameter_name] = self.resolve(parameter_dependency).get_instance()

        return StaticDependency(instance=dependency(**args))
