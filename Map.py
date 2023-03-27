from Hero import *
from utils import getch
        
class Map(object):
    ground="."
    dir={"z":Coord(0,-1),"s":Coord(0,1),"d":Coord(1,0), "q":Coord(-1,0)}
    def __init__(self,size=5,pos=Coord(1,1),hero=None):
        if hero == None:
            self._hero=Hero()
            self._hero.reset()
        else:
            self._hero=hero
        self.size=size
        self._mat=[[Map.ground for i in range(self.size)] for i in range(self.size)]
        self._elem={self._hero:pos}
        for (key, element) in self._elem.items():
            self._mat[element.y][element.x]=key

    def __repr__(self):
        classe=""
        for i in range(self.size):
            for j in range(self.size):
                classe=classe+str(self._mat[i][j])
            classe=classe+'\n'
        return classe
        
    def __len__(self):
        return self.size
        
    def __contains__(self, item):
        if type(item)==Coord:
            if 0<=item.x and 0<=item.y and item.x<self.size and item.y<self.size:
                return True
            else:
                return False
        else:
            if item in self._elem:
                return True
            else:
                return False
            
    def get(self,item): 
        return self._mat[item.y][item.x]
        
        
    def pos(self,item) :
        if item in self._elem:
            return self._elem[item]
            
    def put(self,position,item) :
        self._elem[item]=position
        for (key, element) in self._elem.items():
            self._mat[element.y][element.x]=key
            
    def rm(self,item):
        if type(item)==Coord:
            self._mat[item.y][item.x]=Map().ground
            for (key, element) in self._elem.items():
                if self._mat[item.y][item.x]==self._mat[element.y][element.x]:
                    del self._elem[key]
                    break
        else:
            self._mat[self._elem[item].y][self._elem[item].x]=Map().ground
            for (key, element) in self._elem.items():
                if self._mat[self._elem[item].y][self._elem[item].x]==self._mat[element.y][element.x]:
                    del self._elem[key]
                    break
            
        
    def move(self,objet,way):
        dep=Coord(self.pos(objet).x+way.x,self.pos(objet).y+way.y)
        if dep.x>=0 and dep.y>=0 and dep.x<self.size and dep.y<self.size:
            if self.get(dep)==Map().ground:
                self.rm(objet)
                self.put(dep,objet)
            else:
                if type(self.get(dep))==Element:
                    self.get(dep).meet(self._hero)
                    self.rm(self.get(dep))
                elif type(self.get(dep))==Creature:
                    if self.get(dep).meet(self._hero)==True:
                        self.rm(self.get(dep))
        
                        
                    

         
    def play(self, hero='@'):
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")

