from Equipment import *
from Creature import *
from Hero import *
from Map import *
import copy

class Game(object):
    equipments = { 0: [ Equipment("potion","!"), Equipment("gold","o") ], 1: [ Equipment("sword"), Equipment("bow") ], 2: [ Equipment("chainmail") ] }
    monsters = { 0: [ Creature("Goblin",4), Creature("Bat",2,"W") ], 1: [ Creature("Ork",6,strength=2), Creature("Blob",10) ], 5: [ Creature("Dragon",20,strength=3) ] }
    def __init__(self,hero=None,level=1):
        if hero is None:
            self._hero=Hero()
        else:
            self._hero=hero
        self._level=level
        self._floor=None
        self._message=[]
        
    def buildFloor(self):
        self._floor=Map(hero=self._hero)
        
        
    def addMessage(self,msg):
        self._message.append(msg)
        
        
    def readMessages(self):
        lecture=""
        if self._message is False:
            return ""
        for message in self._message:
            lecture+=str(message)+". "
        self._message.clear()
        return lecture
        
    def randElement(self,collection):
        rarete=random.expovariate(1/self._level)
        menagerie = sorted(collection)
        for i in range(len(menagerie)):
            if menagerie[i]<=rarete and ( menagerie[i]==menagerie[-1] or menagerie[i+1]>rarete):
                menagerieChoisie=menagerie[i]
               
        
        elementChoisi=random.choice(collection[menagerieChoisie])
        elementChoisiMultiple=copy.copy(elementChoisi)
        
        return elementChoisiMultiple
        
        
        
    def randEquipment(self):
        return self.randElement(Game.equipments)
    
    
    def randMonster(self):
        return self.randElement(Game.monsters)
    
    
def theGame(game = Game()):
    return game
        
        