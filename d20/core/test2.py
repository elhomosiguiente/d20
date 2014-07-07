__author__ = 'Zane Thorn'


class Template():
    applies_to = []


class GameObject():
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

