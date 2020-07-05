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
