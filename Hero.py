from Equipment import Equipment
from Creature import Creature

class Hero(Creature):
    def __init__(self,name='Hero',hp=10,abbrv="@",strength=2,inventory=None):
        Creature.__init__(self,name,hp,abbrv,strength)
        if inventory is None:
            self._inventory=[]
        else:
            self._inventory=inventory
    def take(self,elem):
        if isinstance(elem,Equipment)==False:
            raise TypeError('Not an Element')
        self._inventory.append(elem)
    def description(self):
        return Creature.description(self)+str(self._inventory)