from collections import Hashable


class BijectionDict:
    def __init__(self, type1=int, type2=str):
        assert issubclass(type1, Hashable) and issubclass(type2, Hashable)
        self.type1 = type1
        self.type2 = type2
        self.one2two = {}
        self.two2one = {}

    def __getitem_type1__(self, key1):
        return self.one2two[key1]

    def __getitem_type2__(self, key2):
        return self.two2one[key2]

    def __getitem__(self, item):
        if isinstance(item, self.type1):
            return self.__getitem_type1__(item)
        else:
            return self.__getitem_type2__(item)

    def __setitem__(self, key, value):
        if isinstance(value, self.type1):
            key, value = value, key
        self.one2two[key] = value
        self.two2one[value] = key

    def __len__(self):
        return len(self.one2two)
