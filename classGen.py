class BaseClass(object):
    def __init__(self, classtype):
        self._type = classtype

def classGen(name, argnames, BaseClass=BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass