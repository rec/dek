from dek import dek, dex
import unittest


class TestDek(unittest.TestCase):
    def setUp(self):
        self.results = []

        @dek
        def dek_decorator(func, args, kwargs, label='debug'):
            result = func(*args, **kwargs)
            self.results.append((result, args, kwargs, label))
            return result

        @dex
        def dex_decorator(func, label='debug'):
            def wrapped(*args, **kwargs):
                result = func(*args, **kwargs)
                self.results.append((result, args, kwargs, label))
                return result

            return wrapped

        self.dek_decorator = dek_decorator
        self.dex_decorator = dex_decorator

    def test_dex1(self):
        @self.dex_decorator
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dex2(self):
        @self.dex_decorator()
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'debug')]

    def test_dex3(self):
        @self.dex_decorator(label='TEST')
        def func(a, b):
            return a + b

        assert func(1, 2) == 3
        assert self.results == [(3, (1, 2), {}, 'TEST')]

    def test_dex4(self):
        @self.dex_decorator('TEST')
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
