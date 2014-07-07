__author__ = 'Zane Thorn'

try:
    from .base import Score, d6
except SystemError:
    from base import Score, d6

stat_roll = 3*d6
print(stat_roll)

class Stat(Score):
    def __init__(self, base=(3 * d6)()):
        super().__init__(base=base)




class HasStats():
    strength = Stat()
    dexterity = Stat()
    constitution = Stat()


bob = HasStats()
print(bob.strength)
print(dir(bob))