import random

__author__ = 'Zane Thorn'

rnd = random.random()



class DieRoll(tuple):
    __slots__ = []
    def __new__(cls,num=1,sides=0,mod=0):
        if num <= 0:
            raise ValueError('num')
        if sides <= 0:
            raise ValueError('sides')
        return tuple.__new__(cls,(num,sides,mod))
    @property
    def num(self):
        return tuple.__getitem__(self,0)
    @property
    def sides(self):
        return tuple.__getitem__(self,1)
    @property
    def mod(self):
        return tuple.__getitem__(self,2)
    def __getitem__(self, item):
        raise TypeError()
    def __call__(self):
        result = self.mod
        for x in self.num:
            result += rnd.randint(1,self.sides)
        return result
    def __add__(self, other):
        if isinstance(other,int):
            return DieRoll(self.num, self.sides,self.mod+other)
        elif isinstance(DieRoll):
            return CompoundDieRoll(self,other)
    def __sub__(self, other):
        if isinstance(other,int):
            return DieRoll(self.num, self.sides,self.mod-other)
        elif isinstance(DieRoll):
            return CompoundDieRoll(self,-other)
    def __mul__(self, other):
        if isinstance(other,int):
            return DieRoll(self.num * other, self.sides,self.mod)


class CompoundDieRoll(DieRoll):
    __slots__ = []
    def __new__(cls,*args):
        return tuple.__new__(cls,*args)
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