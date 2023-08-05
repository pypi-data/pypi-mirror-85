import functools
import inspect
import json
from kyqlos.exceptions.client import AugmentTypeError


def args_type_check(func):
    @functools.wraps(func)
    def args_type_check_wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        for arg_key, arg_val in sig.bind(*args, **kwargs).arguments.items():
            annot = sig.parameters[arg_key].annotation
            if type(annot) is type:
                request_type = annot
            else:
                request_type = inspect._empty
            if request_type is not inspect._empty and type(arg_val) is not request_type:
                raise AugmentTypeError(
                    type(arg_val), arg_key, request_type)
        return func(*args, **kwargs)
    return args_type_check_wrapper


def is_json_format(line):
    try:
        json.loads(line)
    except json.JSONDecodeError:
        return False
    return True
