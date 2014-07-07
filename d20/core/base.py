import random

__author__ = 'Zane Thorn'

rnd = random.random()


class DieRoll(tuple):
    __slots__ = []

    def __new__(cls, num=1, sides=0, mod=0):
        if num <= 0:
            raise ValueError('num')
        if sides <= 0:
            raise ValueError('sides')
        return tuple.__new__(cls,( num, sides, mod))

    @property
    def num(self):
        return tuple.__getitem__(self, 0)

    @property
    def sides(self):
        return tuple.__getitem__(self, 1)

    @property
    def mod(self):
        return tuple.__getitem__(self, 2)

    def __getitem__(self, item):
        raise TypeError()

    def __call__(self):
        result = self.mod
        for x in self.num:
            result += rnd.randint(1, self.sides)
        return result

    def __add__(self, other):
        if isinstance(other, int):
            return DieRoll(self.num, self.sides, self.mod + other)
        elif isinstance(DieRoll):
            return CompoundDieRoll(self, other)

    def __sub__(self, other):
        if isinstance(other, int):
            return DieRoll(self.num, self.sides, self.mod - other)
        elif isinstance(DieRoll):
            return CompoundDieRoll(self, -other)

    def __mul__(self, other):
        if isinstance(other, int):
            return DieRoll(self.num * other, self.sides, self.mod)
        print(other)

class CompoundDieRoll(DieRoll):
    __slots__ = []

    def __new__(cls, *args):
        return tuple.__new__(cls, *args)

    def __call__(self):
        result = 0
        for x in self:
            result += x()
        return result


d4 = DieRoll(sides=4)
d6 = DieRoll(sides=6)
d8 = DieRoll(sides=8)
d10 = DieRoll(sides=10)
d12 = DieRoll(sides=12)
d20 = DieRoll(sides=20)
d100 = DieRoll(sides=100)


class Score():
    name = None

    def __init__(self, base=0):
        self.base = base

    def __get__(self, instance, owner):
        modifiers = instance.gather_modifiers(self.name)
        val = self.base() if callable(self.base) else self.base
        return val + modifiers

    def __set__(self, instance, value):
        self.base = value


class Template():
    applies_to = []


class GameType(type):
    def __new__(meta, name, bases, dct):
        for key, val in dct.items():
            if isinstance(val, Score):
                val.name = key
        return type.__new__(meta, name, bases, dct)


class GameObject(metaclass=GameType):
    __templates__ = []

    def add_template(self, template):
        for x in template.applies_to:
            if isinstance(self, x) or self.has_template(x):
                break
        else:
            raise TypeError('Template cannot be applied to this type')

        if not template in self.__templates__:
            self.__templates__.append(template)

    def has_template(self, template_type):
        for t in self.__templates__:
            if isinstance(t, template_type):
                return True
        return False

    def __getattr__(self, name):
        for t in self.__templates__:
            if hasattr(t, name):
                return getattr(t, name)
        return AttributeError(name)

    def __setattr__(self, key, value):
        for t in self.__templates__:
            if hasattr(t, key):
                setattr(t, key, value)
        self.__dict__[key] = value

