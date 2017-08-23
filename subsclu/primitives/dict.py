from collections import UserDict

from subsclu.exceptions import InvalidValue


class MyDict(UserDict):
    def __getitem__(self, item):
        if item in self:
            return super().__getitem__(item)
        else:
            raise InvalidValue("no such item in dict")
