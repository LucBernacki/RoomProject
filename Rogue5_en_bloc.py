import random
import copy
import math
from utils import *



class Coord(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __eq__(self,other):
        if self.x==other.x and self.y==other.y :
            return True
        else:
            return False
    def __add__(self,other):
        x=self.x+other.x
        y=self.y+other.y
        return Coord(x,y)
    def __repr__(self):
        coordonnees="<"+str(self.x)+","+str(self.y)+">"
        return coordonnees
        
    def __sub__(self, other):
        x=self.x-other.x
        y=self.y-other.y
        return Coord(x,y)
        
    def distance(self, other):
        longueur=math.sqrt(math.pow((other.x-self.x),2)+math.pow((other.y-self.y),2))
        return longueur
        
    def direction(self, other):
        diff=self.__sub__(other)
        dist=self.distance(other)
        cos=diff.x/dist
        if cos>1/math.sqrt(2):
            return Map.dir["q"]
        if cos<(-1)/math.sqrt(2):
            return Map.dir["d"]
        elif diff.y>0:
            return Map.dir["z"]
        else:
            return Map.dir["s"]
        
        
        

class Element(object):
    def __init__(self,name,abbrv=None):
        self.name=name
        if not abbrv:
            self._abbrv=name[0]
        else:
            self._abbrv=abbrv
    def __repr__(self):
        return self._abbrv
        
    def description(self):
        return "<"+str(self.name)+">"
        
    def meet(self,hero):
        raise NotImplementedError("Not implemented yet")
        hero.take(self)
        return True
        
        
class Stairs(Element):
    def __init__(self,name="Stairs",abbrv="E"):
        Element.__init__(self,name,abbrv)
        
    def meet(self,hero):
        theGame().buildFloor()
        theGame().addMessage("The "+str(hero.name)+" goes down")
     
        
    


class Equipment(Element):
    def __init__(self,name,abbrv=None,usage=None):
        Element.__init__(self,name,abbrv)
        if usage is None:
            self.usage= None
        else:
            self.usage=usage
            
    def use(self,creature):
        if self.usage is not None:
            theGame().addMessage("The "+str(creature.name)+" uses the "+str(self.name))
            return self.usage(self,creature)
            
        else:
            theGame().addMessage("The "+str(self.name)+" is not usable")
            return False
    
    def meet(self,hero):
        hero.take(self)
        theGame().addMessage("You pick up a "+str(self.name))
        return True
    
        

class Creature(Element):
    def __init__(self,name,hp,abbrv=None,strength=1):
        Element.__init__(self,name,abbrv)
        self.hp=hp
        self._strength=strength
    def description(self):
        return Element.description(self)+"("+str(self.hp)+")"
    
    def meet(self,other):
        self.hp-=other._strength
        theGame().addMessage("The "+str(other.name)+" hits the " + str(self.description()))
        if self.hp<=0:
            return True
        else:
            return False

class Hero(Creature):
    def __init__(self,name='Hero',hp=10,abbrv="@",strength=2,inventory=None):
        Creature.__init__(self,name,hp,abbrv,strength)
        if inventory is None:
            self._inventory=[]
        else:
            self._inventory=inventory
     
        self._inventoryComplete=[]
        for i in self._inventory:
            self._inventoryComplete.append(i.name)
    
       
    def take(self,elem):
        if isinstance(elem,Equipment)==False:
            raise TypeError('Not an Element')
        self._inventory.append(elem)
        self._inventoryComplete.append(elem.name)
        
    def description(self):
        return Creature.description(self)+str(self._inventory)
        
    
        
    def fullDescription(self):
        descpart1= "> name : "+str(self.__dict__['_name'])+"\n> abbrv : "+str(self.__dict__['_abbrv'])+"\n> hp : "+str(self.__dict__['hp'])+"\n> strength : "+str(self.__dict__['_strength'])
        descpart2=''
        if len(self.__dict__)>6:
            for (key, element) in self.__dict__.items():
                if key != '_name' and key!= '_abbrv' and key!='hp' and key!='_strength' and key!='_inventoryComplete'and key!='_inventory':
                    unknown=self.__dict__[key]
                    unknownName=key
                    descpart2+="\n> "+str(unknownName)+" : "+str(unknown)
        descpart3="\n> INVENTORY : "+str(self.__dict__['_inventoryComplete'])
        desc=descpart1+descpart2+descpart3
        return desc
        
    def use(self,item):
        if isinstance(item, Equipment)==False:
            raise TypeError("This is not an equipment")
        if item not in self._inventory:
            raise ValueError("You do not possess this item")
        if item.use(self) is True:
            self._inventory.remove(item)
            self._inventoryComplete.remove(item.name)
        
    
        
class Room(object):
    def __init__(self,HautGauche,BasDroit):
        self.c1=HautGauche
        self.c2=BasDroit
    
    def __repr__(self):
        return "["+str(self.c1)+", "+str(self.c2)+"]"
    
    def __contains__(self,objet):
            if objet.x>=self.c1.x and objet.y>=self.c1.y and objet.x<=self.c2.x and objet.y<=self.c2.y:
                return True
            return False
    
    def center(self):
        if self.c1.x==0:
            centreX=self.c2.x
            if (centreX%2)==0:
                centreXF=centreX/2
            centreXF=centreX//2
        else:
            centreX=self.c2.x-self.c1.x
            if (centreX%2)==0:
                centreXF=centreX/2+self.c1.x
            centreXF=centreX//2+self.c1.x

        if self.c1.y==0:
            centreY=self.c2.y-self.c1.y
            if (centreY%2)==0:
                centreYF=centreY/2
            centreYF=centreY//2
        else:
            centreY=self.c2.y-self.c1.y
            if (centreY%2)==0:
                centreYF=centreY/2+self.c1.y
            centreYF=centreY//2+self.c1.y
        
        return Coord(int(centreXF),int(centreYF))
    
    def intersect(self,AutreSalle):
        if AutreSalle.c1 in self or AutreSalle.c2 in self or Coord(AutreSalle.c2.x, AutreSalle.c1.y) in self or Coord(AutreSalle.c1.x, AutreSalle.c2.y) in self or self.c1 in AutreSalle or self.c2 in AutreSalle or Coord(self.c2.x, self.c1.y) in AutreSalle or Coord(self.c1.x, self.c2.y) in AutreSalle:
            return True
        return False
        
        
    def randCoord(self):
        X=random.randint(self.c1.x,self.c2.x)
        Y=random.randint(self.c1.y,self.c2.y)
        return Coord(X,Y)
        
    def randEmptyCoord(self,map):
        stop=0
        while stop==0:
            elem=self.randCoord()
            if elem==self.center() or map.get(elem)!=map.ground:
                stop=0
            else:
                stop=1
        return elem
            
        
        
    
    def decorate(self,map):
        map.put(self.randEmptyCoord(map),theGame().randEquipment())
        map.put(self.randEmptyCoord(map),theGame().randMonster())
        

        



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
                if type(self.get(dep))==Equipment:
                    self.get(dep).meet(self._hero)
                    self.rm(self.get(dep))
                elif type(self.get(dep))==Creature:
                    if self.get(dep).meet(self._hero)==True:
                        self.rm(self.get(dep))
                elif type(self.get(dep))==Stairs:
                    self.get(dep).meet(self._hero)
                    
        
                        
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
                
    def moveMonster(self, element, way):
        """Moves the element in the direction way."""
        orig = self.pos(element)
        dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = element
                self._elem[element] = dest
            elif self.get(dest) != Map.empty and self.get(dest).meet(element) and self.get(dest) != self._hero:
                self.rm(dest)
                
    def moveAllMonsters(self):
        for (key, element) in self._elem.items():
            if isinstance(key,Creature) and isinstance(key,Hero)==False:
                if self._elem[key].distance(self._elem[self._hero])<6:
                    self.moveMonster(key,self._elem[key].direction(self._elem[self._hero]))

        
        
       
    
def heal(creature):
    creature.hp+=3
    return True
    
def teleport(creature, unique):
    roomRandom = random.choice(theGame()._floor._rooms)
    theGame()._floor.moveMonster(creature,roomRandom.randEmptyCoord(theGame()._floor))
    return unique
        
class Game(object):
    _actions = { 'z': lambda hero: theGame().__dict__['_floor'].move(hero,Coord(0,-1)), 's':lambda hero: theGame().__dict__['_floor'].move(hero,Coord(0,1)),'q':lambda hero: theGame().__dict__['_floor'].move(hero,Coord(-1,0)),'d':lambda hero: theGame().__dict__['_floor'].move(hero,Coord(1,0)),'i':lambda hero: theGame().addMessage(hero.fullDescription()),'k': lambda hero: hero.__setattr__('_hp',0),'u': lambda hero: hero.use(theGame().select(hero._inventory)),' ' : lambda hero: None}
    equipments = { 0: [ Equipment("potion","!",usage=heal), Equipment("gold","o") ], 1: [ Equipment("potion","!",usage=teleport),Equipment("sword"), Equipment("bow") ], 2: [ Equipment("chainmail") ], 3: [ Equipment("portoloin","w",usage=teleport)] }
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
        self._floor.put(self._floor._rooms[-1].center(),Stairs())
        self._level=self._level+1
       
        
        
        
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
        
    def select(self,l):
        choicelist=[]
        for element in l:
            choicelist.append(str(l.index(element))+": "+str(element.name))
        MenuChoix="Choose item> "+str(choicelist)
        print(MenuChoix)
        if getch().isdigit()==False:
            return None
        elif int(getch())>l.index(l[-1]):
            return None
        else:
            return l[int(getch())]
            
    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                Game._actions[c](self._hero)
            self._floor.moveAllMonsters()
        print("--- Game Over ---")
        
        
def theGame(game = Game()):
    return game



theGame().play()