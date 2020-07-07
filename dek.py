"""
🗃 dek - the decorator-decorator 🗃
======================================================

``dek`` decorates your decorators to diminish defects and drudgery.

Writing a decorator with parameters needs three levels of function and offers
several opportunities for error, dull drudgery ``dek`` deletes.

EXAMPLE:

Write a decorator ``print_before`` that prints a function's arguments with a
label when it executes

.. code-block:: python

    # Without dek all is confusion

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


    # Things go clearer with dek
    from dek import dek

    @dek
    def print_before(func, label='debug'):
        print(label, func.args, func.keywords)
        return func()


    # Or use defer mode for more control
    @dek(defer=True)
    def print_before(func, label='debug'):
        def wrapped(foo, bar):
            print(label, foo, bar)
            return func(foo, bar)

        return wrapped

NOTES:

Decorators can be called in many ways:

* ``@print_before``
* ``@print_before()``
* ``@print_before('debug')``
* ``@print_before(label='debug')``
* ``@print_before('debug', verbose=True)``

`This article <https://medium.com/better-programming/how-to-write-python\
-decorators-that-take-parameters-b5a07d7fe393>`_ talks more about
decorators that take parameters.

For advanced problems, the PyPi library
`decorator <https://github.com/micheles/decorator/blob/master/docs/\
documentation.md>`_ does not do what ``dek`` does, but does pretty anything
else you could conceive of in a decorator library.

"""
import functools

__all__ = 'dek'
__version__ = '0.10.2'


def _dek(decorator, defer=False, methods=False):
    """
    Implement a decorator that works with or without parameters and
    understands classes.

    dek has two modes, simple and defer.  Simple mode, the default,
    is less work but offers less control.

    * In simple mode, ``decorator`` is a single function that does all the work

    * In defer mode, ``decorator`` is a function that returns a function that
      that does the work.

    .. code-block:: python

       @dek
       def print_before(func, label='debug'):  # simple mode
           print(label, func.args, func.keywords)
           return func()

       @dek(defer=True)
       def print_before(func, label='label'):  # defer mode
           def wrapper(foo, bar):
               if verbose:
                   print(label, foo, bar)
               return func(foo, bar)

           return wrapper

    The ``methods`` parameter says how classes are treated:

    * If ``methods`` is ``False`` then classes are decorated like any callable;
      otherwise, classes are not decorated, but their methods might be.

    * If ``methods`` is ``True`` then only methods whose names start with ``_``
    are decorated

    * If ``methods`` is a string then only methods whose names start
    with that string are decorated (which means that if ``methods`` is
    the empty string, that all methods are decorated)

    * If ``methods`` is a callable then only methods that return true when
    passed to this callable are decorated
    """

    def is_public_method(m):
        return not m.__name__.startswith('_')

    def is_named_method(m):
        return m.__name__.startswith(methods)

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
                if callable(v) and not isinstance(v, type) and is_method(v):
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
