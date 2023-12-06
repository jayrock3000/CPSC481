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
            if item.cost < currentNode.cost:
                currentNode = item
                currentIndex = index

        # Pop current node, add to closed
        openList.pop(currentIndex)
        closedList.append(currentNode)

        # Check if goal found
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent

            if DEBUG == True:
                print("astar func END")
            return path[::-1]

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
                if child == closedChild:
                    continue

            # Create cost values
            child.dist = currentNode.dist + 1
            child.hDist = math.sqrt((child.position[0] - endNode.position[0]) ** 2 ) + ((child.position[1] - endNode.position[1]) ** 2 )
            child.hGrid = hGrid.iat[child.position]
            child.rand = 0      # Random offset variation disabled for now
            child.cost = child.dist + child.hDist + child.hGrid + child.rand

            # Handle children already in open
            for openNode in openList:
                # Skip if new path is longer
                if child == openNode and child.dist > openNode.dist:
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
        hGrid.iat[loc] = hGrid.iat[loc] + 10

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

def main():
        
    # Initialize Grid 
    #   Create dataframe to hold csv path cost grid
    #   Access grid values using grid.iat[0,0], grid.iat[0, 1], etc
    #   Access grid size using grid.shape, and individual dimensions with grid.shape[0] & grid.shape[1]
    grid = pd.read_csv(r"grids - testGrid1.csv")
   
    # Initialize Heuristic Grid
    hGrid = pd.read_csv(r"grids - testGrid2Heuristic.csv")

    visGrid = pd.read_csv(r"grids - testGrid3Path.csv")

    # Test print grids
    print("grid:")
    print(grid)
    print("hGrid:")
    print(hGrid)
 
    
    # Initialize path of traversal
    path = []
    allPaths = []

    # Intialize Agent
    start = (10, 3)
    end = (1, 3)
    tupac = Agent(start)
    if DEBUG == True:
        print("agent initialized with location ", end='')
        print(tupac.getLoc())
        print("end initialized with location ", end='')
        print(end)

    # Perform Initial A* Search
    path = astar(grid, hGrid, start, end)
    allPaths.append(path)

    # Perform Addititional A* Searches
    addlSearches = 4
    for n in range(addlSearches):
        hGrid = increasePathCost(path, hGrid)
        path = astar(grid, hGrid, start, end)
        allPaths.append(path)
    
    #allPaths.reverse()
    print("\n\nAll Paths:")
    count = 1
    for x in allPaths:
        print(f"Path {count}:\n{x}\n")
        visualizePath(x, start, end, visGrid)
        count +=1

    



    """
    # Create second version
    hGrid2 = hGrid.copy()
    hGrid2 = increasePathCost(path, hGrid2)
    path2 = astar(grid, hGrid2, startLoc, endLoc)
    print("\nSecond AStar search complete.\nPath:")
    print(path2)

    # Create third version
    hGrid3 = hGrid2.copy()
    hGrid3 = increasePathCost(path2, hGrid3)
    path3 = astar(grid, hGrid3, startLoc, endLoc)
    print("\nThird AStar search complete.\nPath:")
    print(path3)

    print("\n\nHGRID")
    print(hGrid)

    print("\n\nHGRID2")
    print(hGrid2)

    print("\n\nHGRID3")
    print(hGrid3)
    """

    if DEBUG == True:
        print("\nProgram has closed successfully\n")


########################################################################

if __name__ == "__main__":
    main()