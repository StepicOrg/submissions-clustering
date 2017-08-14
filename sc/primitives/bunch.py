__all__ = ["BunchOfMethodsMixin"]

from redux import frozenbunch


class BunchOfMethodsMixin:
    def __new__(cls, *methods):
        class Inner:
            def __new__(cls):
                return frozenbunch(**{method.__name__: method for method in methods})

        return Inner
