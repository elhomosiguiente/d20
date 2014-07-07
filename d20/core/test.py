__author__ = 'Zane Thorn'





class CategoricalTemplate(type):
    __allow_multiple__ = False

    def __new__(meta, name, bases, dct):
        # if not '__allow_multiple__' in dct:
        #     dct['__allow_multiple__'] = False
        print('calling __new__ template %s' % name)
        return type.__new__(meta, name, (type,), dct)

    def __init__(cls, name, bases, dct):
        print('calling __init__ templace %s' % name)
        return type.__init__(cls, name, (type,), dct)

    def __call__(cls, name, bases, dct):
        for key in dir(cls):
            if not key in dct and key[0] != '_':
                dct[key] = getattr(cls,key)
        return type.__call__(cls,name,bases,dct)

class GameType(type):
    def __new__(meta, name, bases, dct):
        if not '__required__' in dct:
            dct['__required__'] = []
        if not '__optional__' in dct:
            dct['__optional__'] = []
        print('calling __new__ %s' % name)
        return type.__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print('calling __init__ %s' % name)
        return type.__init__(cls, name, bases, dct)

    # def __instancecheck__(cls, instance):


    # def __call__(cls, *args, **kwargs):
    #     print('calling __call__ %s' % list(args))
    #     bases = (cls,) + tuple(map(lambda a: type(a), args))
    #     new_cls = GameType('', bases, {})
    #     return new_cls(*args, **kwargs)

class CharacterClass(metaclass=CategoricalTemplate):
    __allow_multiple__ = True
    level = 1
    def __call__(cls, level):
        instance = super().__call__()
        instance.level = level
        return instance

class Race(metaclass=CategoricalTemplate):
    pass

class Human(metaclass=Race):
    pass

class Fighter(metaclass=CharacterClass):
    pass

class Cleric(metaclass=CharacterClass):
    pass

class GameObject(type):
    def __new__(meta,*args):
        # bases = (cls,) + tuple(map(lambda a: type(a), args))
        # print(bases)
        # new_cls= GameType('', bases,{})
        #
        # return new_cls(*args,**kwargs)
        name =

    def __init__(self, *args):
        required_found = []
        for arg in args:
            targ = type(arg)
            #self.__bases__ += (targ, )
            for required_type in self.__required__:

                if isinstance(targ, required_type):
                    required_found.append(required_type)
                    self.__bases__ += (targ, )
                    # self._add_prop(required_type, arg)
    #
    #
    # def _add_prop(self, type, value):
    #     prop_name = type.__name__
    #     if hasattr(self, prop_name):
    #         if type.allow_multiple:
    #             setattr(self, prop_name, getattr(self, prop_name, []) + [value])
    #         else:
    #             raise TypeError('Multiple Entries for %s found!' % type.__name__)
    #     else:
    #         if type.allow_multiple:
    #             setattr(self, prop_name, [value])
    #         else:
    #             setattr(self, prop_name, value)


class Character(GameObject, Race, CharacterClass):
    __requires__ = [Race, CharacterClass]

    @property
    def level(self):
        return sum(map(lambda c: c.level, self.character_classes))



bob = Character(Human(), Fighter(level=5))

print(type(bob))
print(bob.__class__)
print(isinstance(bob, Human))
print(isinstance(bob,Fighter))
