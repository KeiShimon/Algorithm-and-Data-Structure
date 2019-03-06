#%%
from collections import OrderedDict
from enum import Enum, auto

#%%

class State(Enum):
    unvisited = auto() # White
    visited = auto() # Black
    visiting = auto() # Grey

class Node:
    def __init__(self,key):
        self.id = key
        self.state = State.unvisited
        self.adjacent = OrderedDict()

    def getConnections(self):
        return self.adjacent.keys()

class Graph:
    def __init__(self):
        self.nodes = OrderedDict()

    def addNode(self,num):
        node = Node(num)
        self.nodes[num] = node
        return node
    
    def addEdge(self,source,dest,weight=0):
        if source not in self.nodes:
            self.addNode(source)
        if dest not in self.nodes:
            self.addNode(dest)
        
        self.nodes[source].adjacent[self.nodes[dest]] = weight

def knightGraph(boardSize):
    ktGraph = Graph()

    def posToNodeID(row,col,boardSize):
        return(row * boardSize + col)

    for row in range(boardSize):
        for col in range(boardSize):
            nodeID = posToNodeID(row,col,boardSize)
            newPositions = genLegalMoves(row,col,boardSize)

            for newPosi in newPositions:
                newID = posToNodeID(newPosi[0],newPosi[1],boardSize)
                ktGraph.addEdge(nodeID,newID)
    
    return ktGraph

def genLegalMoves(row,col,boardSize):
    newmoves = []
    moveOffsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),(1,-2),(1,2),(2,-1),(2,1)]

    for offset in moveOffsets:

        x_new = col + offset[0]
        y_new = row + offset[1]

        if x_new < boardSize and x_new > -1:
            if y_new < boardSize and y_new > -1:
                newmoves += [(y_new, x_new)]

    return newmoves

#%%
def knightTour(depth,path,curNode,limit):
    '''
    This is a recursive function to find a path that a knight takes to visit every coordinate on the chess board.
    d: the current depth in the search tree
    path: a list of vertices visited up to this point
    currentNode: the vertex in the graph we wish to explore
    limit: the number of nodes in the path
    '''

    curNode.state = State.visiting
    path.append(curNode)

    if depth < limit:
        done = False
        for neighbor in curNode.getConnections():
            if not done and neighbor.state == State.unvisited:
                done = knightTour(depth+1, path, neighbor, limit)

        if not done:
            path.pop()
            curNode.state = State.unvisited

    else:
        done = True

    return done

g = knightGraph(6)
path = []

flag = knightTour(1,path,g.nodes[3],25)

print(flag)
if path:
    for node in path:
        print(node.id, end=' ')
else:
    print('path is empty')

#%%
