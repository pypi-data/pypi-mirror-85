import inspect
from inspect import Parameter
from typing import Any, Callable, Dict, Iterable, List, Tuple


default_casted_value = {
    int: 0,
    float: 0.0,
    str: "",
    bool: True,
}


def extract_parameters(callable_method: Callable) -> Iterable[Tuple[str, inspect.Parameter]]:
    """Extract the parameters from a callable by utilizing the build-in inspect module"""
    for key, parameter in inspect.signature(callable_method).parameters.items():
        yield key, parameter


def update_parameters(callable_method: Callable, existing_parameters: Dict[str, str], ignore_keys: List[str]) -> Dict[str, str]:
    """Updates parameters with a signature of a callable"""
    extracted_parameters = {
        k: v.default if v.default != Parameter.empty else ""
        for k, v in dict(extract_parameters(callable_method)).items() if k not in ignore_keys
    }
    extracted_parameters.update({k: str(v) for k, v in existing_parameters.items()})
    return extracted_parameters


def cast_parameters(callable_method: Callable, parameters: Dict[str, str]) -> Iterable[Tuple[str, Any]]:
    """Casts parameters with a signature of a callable"""
    extracted_types = {
        k: v.annotation if v.annotation != Parameter.empty else None
        for k, v in dict(extract_parameters(callable_method)).items()
    }
    for k, v in parameters.items():
        if extracted_type := extracted_types.get(k):
            try:
                yield k, extracted_type(v)
            except ValueError:
                yield k, default_casted_value[extracted_type]
        else:
            yield k, v
