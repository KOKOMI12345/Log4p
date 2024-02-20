import warnings

def deprecated(use_func, d_version):
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(f"The '{func.__name__}' function is deprecated, "
                          f"use '{use_func}' instead. Deprecated in version {d_version}.",
                          DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator
