🗃 `dek` - the decorator-decorator 🗃

`dek` decorates your decorators to diminish defects and drudgery.

Writing a Python decorator which takes no parameters isn't hard.

But writing a decorator with parameters is less easy - and more work
if you want to decorate classes, like `unittest.mock.patch` does.

`dek` is a decorator for decorators that does this deftly with a
single tiny function.

## Example 1: a simple decorator with dek

TASK: write a decorator `before` that prints a function's name and its
arguments before it executes.

With `dek`, it's a few lines:

    import dek

    @dek
    def before(pfunc):
        print(pfunc)
        return pfunc()

Done! To use your new decorator:

    @before
    def phone(two, four=4):
        print('Calling', two + two, four * four)

    one(32, four=3)

    # That prints something like:
    #
    # functools.partial(<function phone at 0x7fafa8072b00>, 32, four=3)
    # Calling 64 9

`pfunc` is a [`functools.partial`](
https://docs.python.org/3/library/functools.html#functools.partial),
which represents the function call that `dek` intercepted.  Your code
can call `pfunc` as often as you like, or add or change parameters.

## Example 2: same, without `dek`

    import functools

    def before(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            print(func, args, kwargs)
            return func(*args, **kwargs)

        return wrapped

With `dek` it's a bit less work, but the real advantage comes when you have
a decorator with a parameter.

## Example 3: a decorator with a single optional parameter

Write a decorator `before` that prints a function's name, arguments
_and a label_ before it executes.

With `dek`, it's a trivial change from the previous solution.

    import dek

    @dek
    def before(pfunc, label='dull'):
        print(label, pfunc.func, *pfunc.args)
        return pfunc()

    @before
    def add(x, y):
        return x + y

    @before(label='Exciting!')
    def times(x, y):
        return x * y

    print('Result', add(2, times(2, 3)))

    # Prints:
    #   Exciting! times 2 3
    #   dull add 2 6
    #   Result 8


## Example 4: same, without `dek`

Without `dek` it's actual work that's easy to get wrong.

    import functools

    def before(func=None, label='dull'):
        if func is not None:
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                print(label, func.__name, *args)
                return func(*args, **kwargs)

            return wrapped

        return functools.partial(before, label=label)


## Example 5: Deferred mode

For finer control over function signatures there is deferred mode, which
lets you select what sort of signature you want to expose with a `wrapped`
function that you create.

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

[This article](https://medium.com/p/1277a9ed34dc/) talks more about
decorators that take parameters and about `dek` in general.

For your advanced decorator desires, the PyPi module
[`decorator`](https://github.com/micheles/decorator/blob/master/docs/documentation.md) does not duplicate duties that `dek` does, but does
pretty anything else you could conceive of in a decorator library.


### [API Documentation](https://rec.github.io/dek#dek--api-documentation)
