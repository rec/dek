"""
🗃 dek - the decorator-decorator 🗃
======================================================

``dek`` simplifies writing decorators that take optional parameters.

Writing a decorator that take parameters requires three levels of function and



(See
`this article <https://medium.com/better-programming/how-to-write-python\
-decorators-that-take-parameters-b5a07d7fe393>`_ for more details.)

``dek`` is a tiny library that decorates your decorators to fix these issues.

EXAMPLE:

Write a decorator ``print_before`` that prints a function's arguments with a
label when it executes.

Make sure it works as ``@print_before`` or ``@print_before()`` or
``@print_before(label='debug')``.

.. code-block:: python

    # Without dek all is sadness

    import functools

    def print_before(label='debug'):
        def deferred(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                print(label, args, kwargs)
                return func(*args, **kwargs)

            return wrapped

        if callable(label):
            return deferred(label)
        return deferred


    # Things go better with dek

    from dek import dek

    @dek
    def print_before(func, args, kwargs, label='debug'):
        print(label, args, kwargs)
        return func(*args, **kargs)


    # For finer control over parameters, enjoy ``dek.dex``

    from dek import dex

    @dex
    def print_before(func, label='debug'):
        def wrapped(foo, bar):
            print(label, foo, bar)
            return func(foo, bar)

         return wrapped
"""
import functools

__all__ = 'dek', 'dex'
__version__ = '0.8.0'


def _dek(split, decorator):
    """
    Wrap a decorator so that it can be called with parameters or without,
    and call ``functools.update_wrapper()`` if needed.

    If split is false:

    Decorators must have a signature whose first three parameters are:

       def _decorator(func, args, kwargs, ...):

    where ``func`` is the function being wrapped, ``args`` are the positional
    arguments to ``func``, and kwargs are the keyword arguments to ``func``.

    After that the decorator is free to use any parameters or arguments it
    cares to.
    """

    def decorate(func, *args_d, **kwargs_d):
        if split:
            wrapped = decorator(func, *args_d, **kwargs_d)
        else:

            def wrapped(*args_f, **kwargs_f):
                return decorator(func, args_f, kwargs_f, *args_d, **kwargs_d)

        return functools.update_wrapper(wrapped, func)

    @functools.wraps(decorator)
    def wrapped(*args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return decorate(args[0])

        @functools.wraps(decorator)
        def deferred(func):
            return decorate(func, *args, **kwargs)

        return deferred

    return wrapped


dek = functools.partial(_dek, False)
dex = functools.partial(_dek, True)
