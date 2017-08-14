__all__ = ["BunchOfMethodsMixin"]


class BunchOfMethods:
    def __init__(self, *methods):
        for method in methods:
            setattr(self, method.__name__, method)


class BunchOfMethodsMixin:
    def __new__(cls, *methods):
        class Inner:
            def __new__(cls):
                return BunchOfMethods(*methods)

        return Inner
