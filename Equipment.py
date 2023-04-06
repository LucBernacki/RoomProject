from Element import Element
from Game import theGame
class Equipment(Element):
    def __init__(self,name,abbrv=None):
        Element.__init__(self,name,abbrv)
    
    def meet(self,hero):
        hero.take(self)
        theGame().addMessage("You pick up a "+str(self._name))
        return True