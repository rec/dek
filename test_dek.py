import dek
import unittest


class TestDek(unittest.TestCase):
    def setUp(self):
        self.results = []

        @dek
        def decorator(func, label='debug'):
            result = func()
            self.results.append((result, func.args, func.keywords, label))
            return result

        @dek(defer=True)
        def defer_decorator(func, label='debug'):
            def wrapped(*args, **kwargs):
                result = func(*args, **kwargs)
                self.results.append((result, args, kwargs, label))
                return result

            return wrapped

        self.decorator = decorator
        self.defer_decorator = defer_decorator

    def test_defer1(self):
        @self.defer_decorator
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_defer2(self):
        @self.defer_decorator()
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_defer3(self):
        @self.defer_decorator(label='TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_defer4(self):
        @self.defer_decorator('TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dek1(self):
        @self.decorator
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek2(self):
        @self.decorator()
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek3(self):
        @self.decorator(label='TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dek4(self):
        @self.decorator('TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_classes(self):
        results = []

        @dek(methods=True)
        def decorator(func):
            results.append(func)
            return func()

        @decorator
        class Foo:
            def one(self):
                pass

            def two(self, a, b=False):
                pass

            def _ignored(self):
                pass

        @decorator
        def fn_three(c):
            pass

        foo = Foo()
        foo.one()
        foo._ignored()
        foo.two('hello', b=True)
        fn_three(23)

        one, two, three = results

        assert one.func.__name__ == 'one'
        assert one.args == (foo,)
        assert not one.keywords

        assert two.func.__name__ == 'two'
        assert two.args == (foo, 'hello')
        assert two.keywords == {'b': True}

        assert three.func.__name__ == 'fn_three'
        assert three.args == (23,)
        assert three.keywords == {}

    def test_classes2(self):
        results = []

        @dek(defer=True, methods='test')
        def decorator(func):
            def wrapper(*args, **kwargs):
                results.append((func.__name__, args, kwargs))
                return func(*args, **kwargs)

            return wrapper

        @decorator
        class Foo:
            def test_one(self):
                pass

            def ignored_test(self):
                pass

            def test_two(self, a, b=False):
                pass

        foo = Foo()
        foo.test_one()
        foo.ignored_test()
        foo.test_two('hello', b=True)
        expected = [
            ('test_one', (foo,), {}),
            ('test_two', (foo, 'hello'), {'b': True}),
        ]

        assert results == expected

    def test_classes_callable(self):
        results = []

        def is_method(m):
            from inspect import signature

            return len(signature(m).parameters) > 1

        @dek(methods=is_method)
        def decorator(func):
            results.append(func)
            return func()

        @decorator
        class Foo:
            def one(self, a, b=False):
                pass

            def ignored(self):
                pass

        @decorator
        def fn_two(c):
            pass

        foo = Foo()
        foo.one('hello', b=True)
        foo.ignored()
        fn_two(23)

        one, two = results

        assert one.func.__name__ == 'one'
        assert one.args == (foo, 'hello')
        assert one.keywords == {'b': True}

        assert two.func.__name__ == 'fn_two'
        assert two.args == (23,)
        assert two.keywords == {}

    def test_classes_methods_false(self):
        results = []

        @dek(methods=False)
        def decorator(func):
            results.append(func)
            return func()

        @decorator
        class Foo:
            def one(self):
                pass

            def two(self, a, b=False):
                pass

            def _ignored(self):
                pass

        @decorator
        def fn_three(c):
            pass

        foo = Foo()
        foo.one()
        foo._ignored()
        foo.two('hello', b=True)
        fn_three(23)

        print(results)
        (three,) = results

        assert three.func.__name__ == 'fn_three'
        assert three.args == (23,)
        assert three.keywords == {}

    def test_classes_old(self):
        results = []

        @dek(defer=True)
        def decorator(func):
            # Copied from https://github.com/rec/tdir
            if isinstance(func, type):
                for attr, value in vars(func).items():
                    if attr.startswith('test') and callable(value):
                        setattr(func, attr, decorator(value))

                return func

            def wrapper(*args, **kwargs):
                results.append((func.__name__, args, kwargs))
                return func(*args, **kwargs)

            return wrapper

        @decorator
        class Foo:
            def test_one(self):
                pass

            def not_a_test(self):
                pass

            def test_two(self, a, b=False):
                pass

        foo = Foo()
        foo.test_one()
        foo.not_a_test()
        foo.test_two('hello', b=True)
        expected = [
            ('test_one', (foo,), {}),
            ('test_two', (foo, 'hello'), {'b': True}),
        ]

        assert results == expected
