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
    if DEBUG == True:
        print("startNode and endNode initialized")

    # Create Open & Closed lists
    openList = []
    closedList = []
    if DEBUG == True:
        print("openList and closedList initialized")
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
                        #Sqrt added to compensate for hGrid
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

def main():
        
    # Initialize Grid 
    #   Create dataframe to hold csv path cost grid
    #   Access grid values using grid.iat[0,0], grid.iat[0, 1], etc
    #   Access grid size using grid.shape, and individual dimensions with grid.shape[0] & grid.shape[1]
    grid = pd.read_csv(r"E:\School\Fullerton\2023_ Fall\CPSC 481\CPSC481 Project\CPSC481\grids - testGrid1.csv")
   
    # Initialize Heuristic Grid
    hGrid = pd.read_csv(r"E:\School\Fullerton\2023_ Fall\CPSC 481\CPSC481 Project\CPSC481\grids - testGrid1Heuristic.csv")
    

    # Test print grids
    print("grid:")
    print(grid)
    print("hGrid:")
    print(hGrid)
 
    
    # Initialize path of traversal
    path = []
    if DEBUG == True:
        print("\npath initialized as ", end='')
        print(path)

    # Intialize Agent
    startLoc = (10, 3)
    endLoc = (1, 3)
    tupac = Agent(startLoc)
    if DEBUG == True:
        print("agent initialized with location ", end='')
        print(tupac.getLoc())
        print("endLoc initialized with location ", end='')
        print(endLoc)

    """
    print("\n\nTesting getting values from the grid")
    print(hGrid.iat[1, 3])
    print(hGrid.iat[endLoc])
    """

    # Perform A* Search
    path = astar(grid, hGrid, startLoc, endLoc)
    print("\nAStar search complete.\nPath:")
    print(path)

    print("And some quick tests about specific path values")
    print(path[0])
    print(path[1])
    print(path[2])
    print(f"cost of path[0] is {hGrid.iat[path[0]]}")

    if DEBUG == True:
        print("\nProgram has closed successfully\n")

########################################################################

if __name__ == "__main__":
    main()