from dek import dek, dek2
import unittest


class TestDek(unittest.TestCase):
    def setUp(self):
        self.results = []

        @dek
        def dek_decorator(func, label='debug'):
            result = func()
            self.results.append((result, func.args, func.keywords, label))
            return result

        @dek2
        def dek2_decorator(func, label='debug'):
            def wrapped(*args, **kwargs):
                result = func(*args, **kwargs)
                self.results.append((result, args, kwargs, label))
                return result

            return wrapped

        self.dek_decorator = dek_decorator
        self.dek2_decorator = dek2_decorator

    def test_dek2_1(self):
        @self.dek2_decorator
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek2_2(self):
        @self.dek2_decorator()
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek2_3(self):
        @self.dek2_decorator(label='TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dek2_4(self):
        @self.dek2_decorator('TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dek1(self):
        @self.dek_decorator
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek2(self):
        @self.dek_decorator()
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dek3(self):
        @self.dek_decorator(label='TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dek4(self):
        @self.dek_decorator('TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_classes(self):
        results = []

        @dek2
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
