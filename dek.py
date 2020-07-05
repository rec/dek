"""
🗃 dek - the decorator-decorator 🗃
======================================================

``dek`` makes writing decorators a dream.

Writing a decorator with parameters needs three levels of function and
several opportunities for error. (See
`this article <https://medium.com/better-programming/how-to-write-python\
-decorators-that-take-parameters-b5a07d7fe393>`_ for more details.)

``dek`` decorates your decorators to diminish defects and drudgery.

EXAMPLE:

Write a decorator ``print_before`` that prints a function's arguments with a
label when it executes.

And make sure this works: ``@print_before`` and this: ``@print_before()`` and
this: ``@print_before('debug')`` and this: ``@print_before(label='debug')``.

.. code-block:: python

    # Without dek all is sadness

    import functools

    def print_before(label='label'):
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


    # For finer control, enjoy ``dek.dex``
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


def _dek(is_simple, decorator):
    """Wrap a decorator so that it can be called with parameters or without"""

    def decorate(func, *args_d, **kwargs_d):
        def simple_wrapper(*args_f, **kwargs_f):
            return decorator(func, args_f, kwargs_f, *args_d, **kwargs_d)

        if is_simple:
            wrapper = simple_wrapper
        else:
            wrapper = decorator(func, *args_d, **kwargs_d)

        return functools.update_wrapper(wrapper, func)

    @functools.wraps(decorator)
    def wrapped(*args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return decorate(args[0])

        @functools.wraps(decorator)
        def deferred(func):
            return decorate(func, *args, **kwargs)

        return deferred

    return wrapped


dek = functools.partial(_dek, True)
dex = functools.partial(_dek, False)

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
