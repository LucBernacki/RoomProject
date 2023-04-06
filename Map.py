import random
from Hero import *
from Coord import *
from Room import *
from utils import getch
     
class Map(object):
    empty=" "
    ground="."
    dir={"z":Coord(0,-1),"s":Coord(0,1),"d":Coord(1,0), "q":Coord(-1,0)}
    def __init__(self,size=20,hero=None,SallesDispo=None,Salles=None,nbrooms=7):
        if hero == None:
            self._hero=Hero()
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
        self.nbrooms=nbrooms
        self.generateRooms(self.nbrooms)
        self.reachAllRooms()
        self._elem={self._hero:self._rooms[0].center()} #self._hero:pos
        for (key, element) in self._elem.items():
            self._mat[element.y][element.x]=key
        for rooms in self._rooms:
            rooms.decorate(self)

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
                
    def checkCoord(self,coord):
        if isinstance(coord,Coord)==False:
            raise TypeError('Not a Coord')
        if coord.x>self.size or coord.x<0 or coord.y>self.size or coord.y<0:
            raise IndexError('Out of map coord')
        
        
    def checkElement(self,elem):
        if isinstance(elem,Element)==False:
            raise TypeError('Not an Element')
            
    def get(self,item): 
        self.checkCoord(item)
        return self._mat[item.y][item.x]
        
        
    def pos(self,item) :
        self.checkElement(item)
        return self._elem[item]
       
            
    def put(self,position,item) :
        self.checkCoord(position)
        self.checkElement(item)
        if self.get(position)!=Map.ground:
            raise ValueError('Incorrect cell')
        if item in self._elem:
            raise KeyError('Already placed')
        
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
            self._mat[self._elem[item].y][self._elem[item].x]=Map.ground
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
                self._mat[room.c1.y+j][room.c1.x+i]=Map.ground
                
    
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
        self._mat[coord.y][coord.x]=Map.ground
        if self.findRoom(coord) is not False:
            self._rooms.append(self.findRoom(coord))
            self._roomsToReach.remove(self.findRoom(coord))
            
    def corridor(self, start, end):
        startY=start
        startX=start
        self.dig(start)
        if start.y<end.y:
            for case in range(0,end.y-start.y):
                startY.y=startY.y+1
                self.dig(startY)
        else:
            for case in range(0,start.y-end.y):
                startY.y=startY.y-1
                self.dig(startY)
        
        if start.x<end.x:
            for case in range(0,end.x-start.x):
                startX.x=startX.x+1
                self.dig(startX)
        else:
            for case in range(0,start.x-end.x):
                startX.x=startX.x-1
                self.dig(startX)
                
                
    def reach(self):
        salleDepart=random.choice(self._rooms)
        salleArrive=random.choice(self._roomsToReach)
        self.corridor(salleDepart.center(),salleArrive.center())
        
 
        
    def move(self,objet,way):
        dep=Coord(self.pos(objet).x+way.x,self.pos(objet).y+way.y)
        if dep.x>=0 and dep.y>=0 and dep.x<self.size and dep.y<self.size:
            if self.get(dep)==Map.ground:
                self.rm(objet)
                self.put(dep,objet)
            else:
                if type(self.get(dep))==Element:
                    self.get(dep).meet(self._hero)
                    self.rm(self.get(dep))
                elif type(self.get(dep))==Creature:
                    if self.get(dep).meet(self._hero)==True:
                        self.rm(self.get(dep))
        
                        
    def reachAllRooms(self):
        self._rooms.append(self._roomsToReach[0])
        self._roomsToReach.remove(self._roomsToReach[0])
        while self._roomsToReach:
            self.reach()
            
    def randRoom(self):
        CoX1=random.randint(0,len(self)-3)
        CoY1=random.randint(0,len(self)-3)
        largeur=random.randint(3,8)
        hauteur=random.randint(3,8)
        CoX2=min(len(self)-1,largeur+CoX1)
        CoY2=min(len(self)-1,hauteur+CoY1)
        return Room(Coord(CoX1,CoY1),Coord(CoX2,CoY2))
        
    def generateRooms(self,n):
        for i in range(n):
            SalleACreer=self.randRoom()
            if self.intersectNone(SalleACreer):
                self.addRoom(SalleACreer)

         
    def play(self, hero='@'):
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")
        