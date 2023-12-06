########################################################################
# Project for CPSC 481
# By Jeffrey Rhoten
#
# main.py
#
# DESCRIPTION - WIP
########################################################################

# Import Statements
import pandas as pd
import numpy
import math

# Global Variables
DEBUG = True
MAX_CLOSED = 100


########################################################################

class Agent:
    def __init__(self, X=(0, "A")):
        self.location = X

    def setLoc(self, X):
        self.location = X

    def getLoc(self):
        return self.location 
    

########################################################################

class Node():
    # Adapted from website https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

    # Class defines nodes to be used in A* search

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dist = 0       # Distance from initial node
        self.hDist = 0      # Heuristic value calculated by euclidian linear distance
        self.hGrid = 0      # Heuristic value given by separate heuristic grid
        self.rand = 0       # Random value added to reduce predictability

        self.cost = 0       # Total cost of node, sum(d + hd + hg + r)

    def __eq__(self, other):
        return self.position == other.position

########################################################################
# Function to compare two nodes

def compareNodes(a, b):
    diff = 0.1
    if (a.dist - b.dist) < diff and (a.hDist - b.hDist) < diff and (a.hGrid - b.hGrid) < diff and (a.rand - b.rand) < diff and (a.cost - b.cost) < diff:
        return True

    #if a.position == b.position:
    #    return True
    
    return False

########################################################################

def astar(grid, hGrid, start, end):
    # Adapted from website https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    if DEBUG == True:
        print("astar func START")
        #print("Given values:")
        #print(grid)
        #print(hGrid)
        #print(start)
        #print(end)

    # Create Start & End nodes
    startNode = Node(None, start)
    endNode = Node(None, end)
    
    # Create Open & Closed lists
    openList = []
    closedList = []

    numRows, numColumns = grid.shape
    
    # Add startNode to open
    openList.append(startNode)

    # Loop begins A* search
    while (len(openList) > 0):
        # Get current node (lowest cost node in openList)
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.cost < (currentNode.cost - 0.01):
                currentNode = item
                currentIndex = index

        # Pop current node, add to closed
        openList.pop(currentIndex)
        closedList.append(currentNode)
        #print(f"Size of closed is: {len(closedList)}")

        # Check if goal found
        if currentNode.position == endNode.position:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent

            if DEBUG == True:
                print("astar func END")
            return path[::-1]

        elif len(closedList) > 100:
            path = []
            print("closedList limit exceeded")
            return path

        # Get children
        children = []
        for newPos in [(0, 1), (1, 0), (0, -1), (-1, 0)]:   # Adjacent spaces in taxicab
            
            # Get node position
            nodePos = (currentNode.position[0] + newPos[0], currentNode.position[1] + newPos[1])

            # Ensure within grid range
            if nodePos[0] < 0 or nodePos[0] > numRows or nodePos[1] < 0 or nodePos[1] > numColumns:
                continue

            # Ensure terrain is traversable
            if grid.iat[nodePos] == 0:      # Using 1 for passable terrain, 0 for impassable
                continue

            # Create new node
            newNode = Node(currentNode, nodePos)

            # Append child
            children.append(newNode)
        
        # Loop through children
        for child in children:
            # Catch children already closed
            for closedChild in closedList:
                #if child == closedChild:
                #    continue
                if compareNodes(child, closedChild):
                    continue

            # Create cost values
            child.dist = currentNode.dist + 1
            child.hDist = ((child.position[0] - endNode.position[0]) ** 2 ) + ((child.position[1] - endNode.position[1]) ** 2 )
            #print(f"child.hDist is {child.hDist}")
            child.hGrid = hGrid.iat[child.position]
            child.rand = 0      # Random offset variation disabled for now
            child.cost = child.dist + (child.hDist) + child.hGrid + child.rand

            # Handle children already in open
            for openNode in openList:
                # Skip if new path is longer
                #if child == openNode and child.dist > openNode.dist:
                #    continue
                if compareNodes(child, openNode) and child.dist > (openNode.dist-0.01):
                    continue
            
            # Add child to open list
            openList.append(child)

        #print("adding tuples")
        #pos1 = (5, 5)
        #adjust = (2, 3)
        #pos2 = tuple(numpy.add(pos1, adjust))


########################################################################
# Function for adding random amounts to heuristics

def increasePathCost(path, hGrid):
    if DEBUG == True:
        print("increasePathCost func START")

    shortPath = path.copy()

    # Remove start and end
    shortPath.pop(len(path)-1)
    shortPath.pop(0)


    for loc in shortPath:
        hGrid.iat[loc] = hGrid.iat[loc] + 99

    return hGrid


########################################################################
# Function for printing a basic visualization of a path

def visualizePath(path, start, end, visGrid):
    if DEBUG == True:
        print("visualizePath func START")
    
    thisVis = visGrid.copy()
    for loc in path:
        thisVis.iat[loc] = 22

    thisVis.iat[start] = 11
    thisVis.iat[end] = 33
    
    print(thisVis)


########################################################################
# Simple function for calculating distance

def calcDist(start, end):
    if DEBUG == True:
        print("calcDist func START")

    return math.sqrt((end[0]-start[0])**2 + (end[1] - start[1])**2)


########################################################################

def main():
        
    # Initialize Grid 
    #   Create dataframe to hold csv path cost grid
    #   Access grid values using grid.iat[0,0], grid.iat[0, 1], etc
    #   Access grid size using grid.shape, and individual dimensions with grid.shape[0] & grid.shape[1]
    grid = pd.read_csv(r"grids - testGrid1.csv")
   
    # Initialize Heuristic Grid
    hGrid = pd.read_csv(r"grids - testGrid2Heuristic2.csv")

    visGrid = pd.read_csv(r"grids - testGrid3Path.csv")

    # Test print grids
    #print("grid:")
    #print(grid)
    #print("hGrid:")
    #print(hGrid)
 
    
    # Initialize path of traversal
    path = []
    allPaths = []

    # Intialize Agent
    start = (10, 3)
    end = (1, 7)
    tupac = Agent(start)
    if DEBUG == True:
        print("agent initialized with location ", end='')
        print(tupac.getLoc())
        print("end initialized with location ", end='')
        print(end)

    # Perform Initial A* Search
    path = astar(grid, hGrid, start, end)
    
    print(path)

    allPaths.append(path)
    visualizePath(path, start, end, visGrid)
    
    # Calculate Juke Location
    jukePercent = 0.9           # Distance where juke begine, 1 is start, 0 is destination, 0.5 halfway
    totalDist = calcDist(start, end)    # Dist from start to end
    jukeDist = totalDist * jukePercent  # Dist after which you start juking

    for loc in path:
        dist = calcDist(loc, end)
        if dist-0.01 < jukeDist:
            jukeLocation = loc
            break
    
    pathStart = path[:path.index(jukeLocation)]
    pathEnd = path[path.index(jukeLocation):]
    

    #print(f"\n\njukeLocation was {jukeLocation}")
    #print(f"Actual distance being skipped is {calcDist(jukeLocation, end)}")
    #print(f"pathEnd was {pathEnd}")
    

    
    # Perform Addititional A* Searches
    addlSearches = 5
    for n in range(addlSearches):
        hGrid = increasePathCost(path, hGrid)
        newPath = astar(grid, hGrid, jukeLocation, end)
        path = pathStart + newPath
        if path in allPaths:
            break
        if len(newPath) > 0:
            allPaths.append(path)
    
    print("\n\nAll Paths:")
    count = 1
    for x in allPaths:
        print(f"\n\nPath {count}:\n{x}\n")
        visualizePath(x, start, end, visGrid)
        count +=1
    
    

    if DEBUG == True:
        print("\nProgram has closed successfully\n")


########################################################################

if __name__ == "__main__":
    main()