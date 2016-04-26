#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import inspect

from .dogpile import cache_get
from .dogpile import cache_set


def default_key_fun_impl(fun, *args, **kwargs):
    name = fun.__name__
    mod = fun.__module__
    call_args = inspect.getcallargs(fun, *args, **kwargs)

    return "%s-%s-%s" % (
        name,
        mod,
        '-'.join(
            ["%s-%s" % (k, call_args[k]) for k in sorted(call_args.iterkeys())]
        )
    )


def cacheable(cache, key=None, ttl=60, is_enabled=True):
    """
    Decorator for cacheable function
    """
    def decorator(fxn):
        if callable(key):
            key_fun = key
        else:
            key_fun = default_key_fun_impl if key is None else \
                lambda fxn, *args, **kwargs: key

        @wraps(fxn)
        def wrapper(*args, **kwargs):
            if is_enabled:
                key = key_fun(fxn, *args, **kwargs)
                data = cache_get(cache, key)
                if data is None:
                    data = fxn(*args, **kwargs)
                    cache_set(cache, key, data, ttl)
                return data
            else:
                return fxn(*args, **kwargs)
        return wrapper
    return decorator

# vim: filetype=python
