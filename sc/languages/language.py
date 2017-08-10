__all__ = ["Language"]


# TODO: forbid to change language class
class Language:
    def __init__(self, *methods):
        for method in methods:
            setattr(self, method.__name__, method)

    @staticmethod
    def from_str(language):
        if language == "python":
            from .python import Python
            return Python()
        else:
            raise ValueError("No such language supported yet")

    def __getitem__(self, item):
        return self.__dict__[item]

    @property
    def methods(self):
        return list(self.__dict__.keys())
