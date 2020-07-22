"""
🗃 dek - the decorator-decorator 🗃
======================================================

``dek`` decorates your decorators to diminish defects and drudgery.

Writing a Python decorator which takes no parameters is easy.

But writing a decorator with parameters requires three nested levels of
function and offers several opportunities for error - and more work
if you want to decorate classes like ``unittest.mock.patch`` does.

``dek`` is a decorator for decorators that does this deftly with a single
tiny function.

EXAMPLE
---------

Write a decorator ``print_before`` that prints a function's arguments with an
optional label before it executes.

Without ``dek`` all is confusion:

.. code-block:: python

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

``dek`` handles all the boilerplate:

.. code-block:: python

    import dek

    @dek
    def print_before(pfunc, label='debug'):
        print(label, pfunc)
        return pfunc()


For finer control over function signatures there is deferred mode:

.. code-block:: python

    @dek(defer=True)
    def print_before(func, label='debug'):

        def wrapped(foo, bar):
            print(label, foo, bar)
            return func(foo, bar)

        return wrapped

NOTES:

`This article <https://medium.com/p/1277a9ed34dc/>`_ talks more about
decorators that take parameters and about ``dek`` in general.

For your advanced decorator problems, the PyPi module
`decorator <https://github.com/micheles/decorator/blob/master/docs/\
documentation.md>`_ does not duplicate duties that ``dek`` does, but does
pretty anything else you could conceive of in a decorator library.

"""
import functools
import xmod

__all__ = ('dek',)
__version__ = '0.10.5'


def _dek(decorator, defer=False, methods=None):
    """
    Decorate a decorator so it works with or without parameters and
    can decorate all the members of a class.

    ARGUMENTS
      decorator
        The function being decorated

      defer
        Switch between "simple" and "defer" modes

      methods
        What to do with class methods when wrapping a class

    dek has two modes, simple and deferred.  Simple mode, the default,
    is less work but offers less control.

    In **simple mode** the trivial decorator, the decorator that does nothing,
    is trivial to write:

    .. code-block:: python

       @dek
       def trivial(pfunc):
           return pfunc()

    In this mode, ``decorator``'s first argument is ``pfunc``,
    a ``functools.partial()`` which bundles the original function together with
    its arguments.

    Decorators with parameters aren't much harder:

    .. code-block:: python

       @dek
       def print_before(pfunc, label='debug'):
           print(label, pfunc)
           return pfunc()

       @print_before
       def do_stuff(a, b='default'):
          # do stuff

       do_stuff(1)
       # also prints 'debug do_stuff 1'

    ----------------

    In **deferred mode**, ``decorator`` is a function that returns a function
    that does the work.  This is more code but more flexible.

    .. code-block:: python

       @dek(defer=True)
       def trivial(func):
           def wrapper(*args, **kwargs):
               return func(*args, **kwargs)

           return wrapper

       @dek(defer=True)
       def print_before(func, label='label'):
           def wrapper(foo, bar):
               print(label, foo, bar)
               return func(foo, bar)

           return wrapper

    --------

    The ``methods`` parameter describe how classes (as opposed to functions or
    methods) are decorated.

    * If ``methods`` is ``None`` then classes are decorated like any callable.
      If ``methods`` is _not_ ``None`` then classes are not decorated.

    * If ``methods`` is a string, then only methods whose names start
      with that string are decorated (which means that if ``methods`` is
      the empty string, that all methods are decorated).

    * If ``methods`` is a callable, then only methods that return true when
      passed to the callable are decorated.

    * If ``methods`` is ``True``, then only public, non-magic methods - methods
      whose names do *not* start with ``_`` - are decorated.

    * If ``methods`` is ``False``, then methods are not decorated (and neither
      is the class).
    """

    def is_public_non_magic_method(m):
        return not m.__name__.startswith('_')

    def is_named_method(m):
        return m.__name__.startswith(methods)

    def no_method(m):
        return False

    if methods is not None:
        if callable(methods):
            is_method = methods
        elif methods is True:
            is_method = is_public_non_magic_method
        elif methods is False:
            is_method = no_method
        elif isinstance(methods, str):
            is_method = is_named_method
        else:
            raise TypeError('Do not understand methods=%s' % methods)

    def decorate(func, *args_d, **kwargs_d):
        if methods is not None and isinstance(func, type):
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
xmod(dek)
