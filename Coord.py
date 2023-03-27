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
