from subsclu.exceptions import InvalidSpec, InvalidValue
from subsclu.primitives import BunchOfFuntions

__all__ = ["Language"]


class Language:
    def __init__(self, methods):
        self._bof = BunchOfFuntions(methods)

    def __contains__(self, item):
        return item in self.__dict__ or item in self._bof.__dict__

    def __getitem__(self, item):
        if item in self:
            return self.__dict__.get(item, self._bof.__dict__.get(item))
        else:
            raise InvalidValue("no such field or method in language")

    @staticmethod
    def outof(name):
        from .spec import NAME_TO_LANGUAGE as name_mapping
        if name in name_mapping:
            return name_mapping[name]
        else:
            raise InvalidSpec("name must be one of the {}".format(name_mapping.keys()))
