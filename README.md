# 🗃 `dek` - the decorator-decorator 🗃

`dek` decorates your decorators to diminish defects and drudgery.

Writing a Python decorator which takes no parameters isn't hard.

But writing a decorator with parameters is less easy - and more work
if you want to decorate classes, like `unittest.mock.patch` does.

`dek` is a decorator for decorators that does this deftly with a
single tiny function.

## Example 1: a simple decorator with dek

Write a decorator `before` that prints a function's arguments with a
label before it executes.

With `dek`, it's a few lines:

    import dek

    @dek
    def before(pfunc):
        print(pfunc.func.__name__)
        return pfunc()

Done! To use your new decorator:

    @before
    def phone(two, four=4):
        print('Calling', two + two, four * four)

    one(32, four=3)

    # That prints something like:
    #
    # hey: functools.partial(<function phone at 0x7fafa8072b00>, 32, four=3)
    # Calling 64 9

(What's `pfunc`?  It is a `functools.partial` that represents the function call
that `dek` intercepted - a convenient way to hold the arguments and keyword
arguments to the function you are decorating.)

## Example 2: same, without `dek`

    import functools

    def before(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            print(args, kwargs)
            return func(*args, **kwargs)

        return wrapped

With `dek` it's a bit less work, but the real advantage comes when you have
a decorator with a parameter.

## Example 3: a decorator with a single optional parameter

Write a decorator `before` that prints a function's arguments _with a
label_ before it executes.

With `dek`, it's a trivial change from the previous one.

    import dek

    @dek
    def before(pfunc, label='my label'):
        print(label, pfunc.func.__name__)
        return pfunc()

And you get an optional label.

    @before
    def add(x, y):
        return x + y

    @before(label='Exciting!')
    def times(x, y):
        return x * y


## Example 4: same, without `dek`

Without `dek` it's actual work that's easy to get wrong.

    import functools

    def before(func=None, label='label'):
        if func is not None:
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                print(label, args, kwargs)
                return func(*args, **kwargs)

            return wrapped

        return functools.partial(before, label=label)


## Example 5: Deferred mode

For finer control over function signatures there is deferred mode.

    @dek(defer=True)
    def before(func, label='debug'):
        def wrapped(foo, bar):
            print(label, foo, bar)
            return func(foo, bar)

        return wrapped

## Example 6: Decorating a class

If you need to decorate methods on a class, there's a `methods` parameter to
select which methods get decorated.


    import dek

    @dek(methods='test')
    def before(pfunc):
        print('HERE', *pfunc.args)
        return pfunc()

    @before
    class Class:
        def test_one(self):
            return 1

        def test_two(self):
            return 2

        def three(self):  # This won't get decorated
            return 1


    # Test at the command line:
    >>> cl = Class()
    >>> cl.test_one(), cl.test_two(), cl.three()
    HERE 1
    HERE 2
    (1, 2, 3)

NOTES:

`This article <https://medium.com/p/1277a9ed34dc/>`_ talks more about
decorators that take parameters and about `dek` in general.

For your advanced decorator problems, the PyPi module
`decorator <https://github.com/micheles/decorator/blob/master/docs/documentation.md>`_ does not duplicate duties that `dek` does, but does
pretty anything else you could conceive of in a decorator library.


### [API Documentation](https://rec.github.io/dek#dek--api-documentation)
