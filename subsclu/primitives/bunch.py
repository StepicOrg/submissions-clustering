from subsclu.exceptions import InvalidValue


class BunchOfFuntions:
    def __init__(self, functions):
        for names, function_ in functions:
            if not isinstance(names, tuple):
                names = (names,)
            for name in names:
                self.__dict__[name] = function_

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise InvalidValue("no such function in bunch")
