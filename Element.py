from Room import Room
class Element(object):
    def __init__(self,name,abbrv=None):
        self._name=name
        if not abbrv:
            self._abbrv=name[0]
        else:
            self._abbrv=abbrv
    def __repr__(self):
        return self._abbrv
        
    def description(self):
        return "<"+str(self._name)+">"
        
    def meet(self,hero):
        hero.take(self)
        return True