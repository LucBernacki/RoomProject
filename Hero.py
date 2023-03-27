from Creature import *

class Hero(Creature):
    def __init__(self,name="Hero",hp=10,abbrv="@",strength=2,inventory=[]):
        Creature.__init__(self,name,hp,abbrv,strength)
        self._inventory=inventory
    def take(self,elem):
        self._inventory.append(elem)
    def description(self):
        return Creature.description(self)+str(self._inventory)
    def reset(self):
        self._name="Hero"
        self._hp=10
        self._abbrv="@"
        self._strength=2
        self._inventory=[]