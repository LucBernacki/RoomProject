from Coord import Coord

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