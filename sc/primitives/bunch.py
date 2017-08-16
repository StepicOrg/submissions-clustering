from redux import frozenbunch

__all__ = ["BunchOfMethods"]


class BunchOfMethods:
    def __new__(cls, *methods):
        class Inner:
            def __new__(cls):
                return frozenbunch(**{method.__name__: method for method in methods})

        return Inner
