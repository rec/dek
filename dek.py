"""
🗃 dek - the decorator-decorator 🗃
======================================================

* ``dek``


EXAMPLE: as a decorator for tests

.. code-block:: python

    from pathlib import Path
    import dek
    import unittest

    CWD = Path().absolute()


    # Decorate a whole class so each test runs in a new temporary directory
    @dek('a', foo='bar')
    class MyTest(unittest.TestCast):
        def test_something(self):
            assert Path('a').read_text() = 'a\n'
            assert Path('foo').read_text() = 'bar\n'


    # Decorate single tests
    class MyTest(unittest.TestCast):
        @dek(foo='bar', baz=bytes(range(4)))
        def test_something(self):
            assert Path('foo').read_text() = 'bar\n'
            assert Path('baz').read_bytes() = bytes(range(4)))

        # Run in an empty temporary directory
        @dek
        def test_something_else(self):
            assert not Path('a').exists()
            assert Path().absolute() != CWD
"""

__all__ = ('dek',)
__version__ = '0.8.0'


def dek(*args, cwd=True, **kwargs):
    """
    A context manager to create and fill a temporary directory.

    ARGUMENTS
      args:
        A list of strings or dictionaries.  For strings, a file is created
        with that string as name and contents.  For dictionaries, the contents
        are used to recursively create and fill the directory.

      cwd:
        If true, change the working directory to the temp dir at the start
        of the context and restore the original working directory at the end.

      kwargs:
        A dictionary mapping file or directory names to values.
        If the key's value is a string it is used to file a file of that name.
        If it's a dictionary, its contents are used to recursively create and
        fill a subdirectory.
    """
    pass
