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

def astar(grid, hGrid, start, end, debug):
    if debug == True:
        print("astar func Begin")
        #print("Given values:")
        #print(grid)
        #print(hGrid)
        #print(start)
        #print(end)

    # Create Start & End nodes
    startNode = Node(None, start)
    endNode = Node(None, end)
    if debug == True:
        print("startNode and endNode initialized")

    # Create Open & Closed lists
    openList = []
    closedList = []
    if debug == True:
        print("openList and closedList initialized")
    
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
        import numpy
        children = []
        for newPos in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            #WIP WIP WIP
            return

        #print("adding tuples")
        #pos1 = (5, 5)
        #adjust = (2, 3)
        #pos2 = tuple(numpy.add(pos1, adjust))


        # Loop through children
    

    if debug == True:
        print("astar func End")
    return

########################################################################

def main():
    debug = True

    # Import Libraries
    import pandas as pd

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
    if debug == True:
        print("\npath initialized as ", end='')
        print(path)

    # Intialize Agent
    startLoc = (10, 3)
    endLoc = (1, 3)
    tupac = Agent(startLoc)
    if debug == True:
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
    astar(grid, hGrid, startLoc, endLoc, debug)

    if debug == True:
        print("\nProgram has closed successfully\n")

########################################################################

if __name__ == "__main__":
    main()