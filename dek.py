"""
🗃 dek - the decorator-decorator 🗃
======================================================

``dek`` decorates your decorators to diminish defects and drudgery.

Writing a decorator with parameters needs three levels of function and
several opportunities for error, which ``dek`` deletes.

EXAMPLE:

Write a decorator ``print_before`` that prints a function's arguments with a
label when it executes

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
    def print_before(func, label='debug'):
        print(label, func.args, func.keywords)
        return func()


    # For finer control, enjoy ``dek.dek2``
    from dek import dek2

    @dek2
    def print_before(func, label='debug'):
        def wrapped(foo, bar):
            print(label, foo, bar)
            return func(foo, bar)

        return wrapped

NOTES:

All these forms are supported:

1. ``@print_before``
2. ``@print_before()``
3. ``@print_before('debug')``
4. ``@print_before(label='debug')``
5. ``@print_before('debug', verbose=True)``

`This article <https://medium.com/better-programming/how-to-write-python\
-decorators-that-take-parameters-b5a07d7fe393>`_ talks more about
decorators that take parameters.

For advanced problems, the PyPi library
`decorator <https://github.com/micheles/decorator/blob/master/docs/\
documentation.md>`_ does not do what ``dek`` does, but does pretty anything
else you could conceive of in a decorator library.

"""
import functools

__all__ = 'dek', 'dek2'
__version__ = '0.10.2'


def _dek(decorator, defer=False, methods=False):
    def is_public_method(m):
        return not m.startswith('_')

    def is_named_method(m):
        return m.startswith(methods)

    if methods:
        if callable(methods):
            is_method = methods
        elif methods is True:
            is_method = is_public_method
        else:
            assert isinstance(methods, str)
            is_method = is_named_method

    def decorate(func, *args_d, **kwargs_d):
        if methods and isinstance(func, type):
            for k, v in vars(func).items():
                if callable(v) and not isinstance(v, type) and is_method(k):
                    setattr(func, k, decorate(v, *args_d, **kwargs_d))
            return func

        def simple_wrapper(*args_f, **kwargs_f):
            f = functools.partial(func, *args_f, **kwargs_f)
            return decorator(f, *args_d, **kwargs_d)

        if defer:
            wrapper = decorator(func, *args_d, **kwargs_d)
        else:
            wrapper = simple_wrapper

        if not isinstance(func, type):
            functools.update_wrapper(wrapper, func)
        return wrapper

    @functools.wraps(decorator)
    def wrapped(*args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return decorate(args[0])

        @functools.wraps(decorator)
        def deferred(func):
            return decorate(func, *args, **kwargs)

        return deferred

    return wrapped


dek = _dek(_dek, defer=True)
dek2 = dek(defer=True)

dek.__doc__ = """
Implement a decorator with parameters, from a simple function

The function ``decorator`` has signature ``decorator(func, ...)``
where ``func`` is a ``functools.partial`` of the call that is
being handled, and the remaining

EXAMPLE:

.. code-block:: python

    @dek
    def print_before(func, label='debug'):
        print(label, func.args, func.keywords)
        return func()
"""

dek2.__doc__ = """
Implement a decorator with parameters, from a function that returns
a function.

The top-level function ``decorator`` has signature ``decorator(func, ...)``
where ``func`` is the function being wrapped. The wrapper function
that's returned can have any signature needed.

EXAMPLE:

.. code-block:: python

    @dek2
    def print_before(func, label='label'):
        def wrapper(foo, bar):
            if verbose:
                print(label, foo, bar)
            return func(foo, bar)

        return wrapper
"""
