from Element import *

class Creature(Element):
    def __init__(self,name,hp,abbrv=None,strength=1):
        Element.__init__(self,name,abbrv)
        self._hp=hp
        self._strength=strength
    def description(self):
        return Element.description(self)+"("+str(self._hp)+")"
    
    def meet(self,other):
        self._hp-=other._strength
        if self._hp<=0:
            return True
        else:
            return False