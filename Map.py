from Hero import *
from Coord import *
from utils import getch
       
class Map(object):
    empty=" "
    ground="."
    dir={"z":Coord(0,-1),"s":Coord(0,1),"d":Coord(1,0), "q":Coord(-1,0)}
    def __init__(self,size=20,pos=Coord(1,1),hero=None,SallesDispo=None,Salles=None):
        if hero == None:
            self._hero=Hero()
            self._hero.reset()
        else:
            self._hero=hero
        if SallesDispo is None:
            self._roomsToReach=[]
        else:
            self._roomsToReach=SallesDispo
        if Salles is None:
            self._rooms=[]
        else:
            self._rooms=Salles
        self.size=size
        self._mat=[[Map.empty for i in range(self.size)] for i in range(self.size)]
        self._elem={} #self._hero:pos
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
                
                
    def addRoom(self,room):
        horizontale=room.c2.x-room.c1.x+1
        verticale=room.c2.y-room.c1.y+1
        self._roomsToReach.append(room)
        for i in range(horizontale):
            for j in range(verticale):
                self._mat[room.c1.y+j][room.c1.x+i]=Map().ground
                
    
    def findRoom(self,coord):
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False
        
    def intersectNone(self,otherRoom):
        quota=0
        for i in range (0,len(self._roomsToReach)):
            if otherRoom.intersect(self._roomsToReach[i])==False:
                quota=quota+1
        if quota==len(self._roomsToReach):
            return True
        else:
            return False
            
    def dig(self,coord):
        self._mat[coord.y][coord.x]=Map().ground
        if self.findRoom(coord) is not False:
            self._rooms.append(self.findRoom(coord))
            self._roomsToReach.remove(self.findRoom(coord))
            
    def corridor(self, start, end):
        startY=start
        startX=start
        if start.y<end.y:
            for case in range(1,end.y-start.y):
                startY.y=start.y+case
                self.dig(startY)
        else:
            for case in range(1,start.y-end.y):
                startY.y=start.y-case
                self.dig(startY)
        
        if start.x<end.x:
            for case in range(1,end.x-start.x):
                startX.x=start.x+case
                self.dig(startX)
        else:
            for case in range(1,start.x-end.x):
                startX.x=start.x-case
                self.dig(startX)
 
        
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