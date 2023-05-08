import theGame
from Map import Map


g = theGame.theGame()
g.buildFloor()
Map.play(g._floor)


