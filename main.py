########################################################################
# Project for CPSC 481
# By Jeffrey Rhoten
#
# main.py
########################################################################

# Import Statements
import pandas as pd
import numpy
import math
import os

# Global Variables
DEBUG = False       # Debug mode provides additional console messages for troubleshooting
MAX_CLOSED = 100    # Cap on size of closed list in case algorithm starts an infinite loop
MAX_FILENAME = 100

########################################################################
# Information header printed when program first runs

def programHeader():
    if DEBUG == True:
        print("programHeader func START")

    print("##################################################")
    print("Project for CPSC 481")
    print("By Jeffrey Rhoten\n")
    print("main.py\n")
    print("Please note that files used for grid must be .csv")
    print("##################################################\n")


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

        # Catch an infinitely expanding closedList - this is a bug fix
        elif len(closedList) > MAX_CLOSED:
            path = []
            #print("closedList limit exceeded")
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


########################################################################
# Function for increasing the cost of the previous path
# so subsequent runs will be forced to find another

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
# Parent function for performing multiple A* Searches

def multiAStar(grid, hGrid, visGrid, start, end, juke, searches):
    # Initialize path of traversal
    path = []
    allPaths = []

    # Perform Initial A* Search
    path = astar(grid, hGrid, start, end)
    
    
    # Perform additional searches if requested by user
    if searches > 1:
        allPaths.append(path)

        # Calculate Juke Location
        jukePercent = juke          # Distance where juke begine, 1 is start, 0 is destination, 0.5 halfway
        totalDist = calcDist(start, end)    # Dist from start to end
        jukeDist = totalDist * jukePercent  # Dist after which you start juking

        for loc in path:
            dist = calcDist(loc, end)
            if dist-0.01 < jukeDist:
                jukeLocation = loc
                break
        
        pathStart = path[:path.index(jukeLocation)]
        pathEnd = path[path.index(jukeLocation):]

        # Perform Addititional A* Searches
        addlSearches = searches-1
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
        
        print(f"\nSearches complete. Algorithm was able to find {count-1} paths, visualized above")
    
    else:
        print(path)
        visualizePath(path, start, end, visGrid)
        print("\nSearch complete. A* search found a path, visualized above")


########################################################################
# Function returns list of files in the given location

def getFileList():
    if DEBUG == True:
        print("getFileList func START")

    # Uses folder called grids located in same folder as this .py
    directory = 'grids'

    # Check directory exists
    if os.path.exists(directory) and os.path.isdir(directory):

        # Retrieve list of files in directory
        files = os.listdir(directory)
        #files = '\n- ' + '\n- '.join(files) + '\n'

        # Return list of files
        return files

    # Or return error message if directory not found
    else:
        return 'Directory not found'


########################################################################
# Function for getting start/end locations

def getNewLocation(locType, rows, columns):
    if DEBUG == True:
        print("getStart func START")

    print("\t*Please note that invalid entries may have unintended effects")

    if locType == "start":
        print("Please enter a start location")
        
    elif locType == "end":
        print("Please enter an end location")

    prompt = "Row: "
    row = intInput(prompt, 0, rows-1)
    prompt = "Column: "
    column = intInput(prompt, 0, columns-1)

    return (row, column)


########################################################################
# Function for getting juke percentage

def getJuke():
    if DEBUG == True:
        print("getJuke func START")
    
    print("Enter a new juke percentage")
    print("Valid inputs 0-100")
    print("0 is starting location, 100 ending location\n")

    prompt = "Juke: "
    jukePercent = intInput(prompt, 0, 100)

    if jukePercent < 1:
        jukePercent = 1
        print("Algorithm expects a minimum juke percentage of 1, so converting to 1%")
    elif jukePercent > 99:
        jukePercent = 99
        print("Algorithm expects a maximum juke percentage of 99, so converting to 99%")

    
    juke = (100-jukePercent) / 100

    return juke


########################################################################
# Function for getting number of search attempts from user

def getSearchAttempts():
    if DEBUG == True:
        print("getSearchAttempts func START")

    print("Enter the number of search attempts you would like to perform")
    print("\n*Please note the algorithm cannot produce more than 4 unique paths")

    prompt = ("Search attempts: ")
    searches = intInput(prompt, 1, 4)

    return searches


########################################################################
# Function for determining which grids will be searched

def getGrids(allGrids):
    if DEBUG == True:
        print("getGrids func START")

    gridName = allGrids[0]
    hGridName = allGrids[1]
    visGridName = allGrids[2]
    
    print("\n*Please note that invalid grids may have unintended results")


    # Get new Navigation grid
    print(f"\nCurrent navigation grid:\n\t{allGrids[0]}")
    print("\nPlease either enter a new file name or quit to skip to cost grids\n")
    
    while True:
        try:
            prompt = "Your selection: "
            userInput = stringInput(prompt, 1, MAX_FILENAME)
            #print(f"You entered: {userInput}")

            if userInput.lower() == "quit":
                break

            elif fileExists(userInput) == True:
                gridName = userInput
                break
            print(f"\nThe file {userInput} couldn't be located in the grids folder. Please try again.\n")

        except:
            print("An unknown error has occurred. Returning to main menu")
            return allGrids

    # Get new Cost grid
    print(f"\nCurrent cost grid:\n\t{allGrids[1]}")

    print("\nPlease either enter a new file name or quit to skip to visualization grids\n")
    
    while True:
        try:
            prompt = "Your selection: "
            userInput = stringInput(prompt, 1, MAX_FILENAME)
            #print(f"You entered: {userInput}")

            if userInput.lower() == "quit":
                break

            elif fileExists(userInput) == True:
                hGridName = userInput
                break
            print(f"\nThe file {userInput} couldn't be located in the grids folder. Please try again.\n")

        except:
            print("An unknown error has occurred. Returning to main menu")
            return allGrids

    # Get new Visualization grid
    print(f"\nCurrent visualization grid:\n\t{allGrids[2]}")

    print("\nPlease either enter a new file name or quit to cancel\n")
    
    while True:
        try:
            prompt = "Your selection: "
            userInput = stringInput(prompt, 1, MAX_FILENAME)
            #print(f"You entered: {userInput}")

            if userInput.lower() == "quit":
                break

            elif fileExists(userInput) == True:
                visGridName = userInput
                break
            print(f"\nThe file {userInput} couldn't be located in the grids folder. Please try again.\n")

        except:
            print("An unknown error has occurred. Returning to main menu")
            return allGrids

    
    newGrids = [gridName, hGridName, visGridName]
    return newGrids



def fileExists(fileName):
    if DEBUG == True:
        print("fileExists func START")
    
    # Directory that will be checked for file
    directory = 'grids'
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    # Look for file in the directory
    while(True):
        try:
            if fileName in files:
                return True
            
            # Catch nonexistant file
            else:
                return False
        
        # Catch nonexistant directory
        except:
            return False
    
    # Backup catch nonexistant file
    return False


########################################################################
# Input validation functions

# Handles user input of integer values
def intInput(prompt, minInt, maxInt):
    if DEBUG == True:
        print("intInput func START")

    userInput = minInt - 1

    while True:
        print(prompt, end="")
        userInput = input()
        try:
            userInput = int(userInput)
        except:
            print("Entry must be a whole number.\n")
            continue
        if userInput < minInt:
            print("Sorry, minimum value is " + str(minInt) + "\n")
            continue
        elif userInput > maxInt:
            print("Sorry, maximum value is " + str(maxInt) + "\n")
            continue
        break
    return userInput

# Handles user input of strings
def stringInput(prompt, minLength, maxLength):
    if DEBUG == True:
        print("stringInput func START")

    userInput = ""

    while True:
        print(prompt, end="")
        userInput = input()
        try:
            userInput = str(userInput)
        except:
            print("Sorry, it looks like that wasn't a valid entry. Please try again.\n")
            continue
        if userInput == "":
            print("Entry cannot be blank\n")
            continue

        elif len(userInput) < minLength:
            print("Sorry, minimum number of characters is " + str(minLength) + "\n")
            continue

        elif len(userInput) > maxLength:
            print("Sorry, maximum number of characters is " + str(maxLength) + "\n")
            continue
        break
    return userInput


########################################################################
# Main menu function

def displayMainMenu(grid, hGrid, visGrid, start, end, juke, searches):
    if DEBUG == True:
        print("displayMainMenu func START")
    
    counter = 1

    print("\nMain Menu\n")
    print(f"{counter}. Run Search")
    counter += 1
    print(f"{counter}. Select grid files\t\tcurrent: {grid}, {hGrid}, {visGrid}")
    counter += 1
    print(f"{counter}. Select starting location\tcurrent: {start}")
    counter += 1
    print(f"{counter}. Select ending location\tcurrent: {end}")
    counter += 1
    print(f"{counter}. Select juke distance\t\tcurrent: {juke}%")
    counter += 1
    print(f"{counter}. Select # of search attempts\tcurrent: {searches}")
    counter += 1
    print(f"{counter}. Exit\n")


########################################################################

def main():
    if DEBUG == True:
        print("main func START")

    # Print header to provide program info
    programHeader()

    # Initialize Grids
    #   Access grid values using grid.iat[0,0], grid.iat[0, 1], etc

    # File folder grids will be located at
    directory = "grids"

    # Grid for determining whether a node is navigable
    gridName = "sampleGrid-navigable.csv"
    gridPath = os.path.join(directory, gridName)
    grid = pd.read_csv(gridPath)

    # Grid for determining cost of a node
    hGridName = "sampleGrid-cost.csv"
    hGridPath = os.path.join(directory, hGridName)
    hGrid = pd.read_csv(hGridPath)

    # Grid for printing visualization of the path
    visGridName = "sampleGrid-visGrid.csv"
    visGridPath = os.path.join(directory, visGridName)
    visGrid = pd.read_csv(visGridPath)

    allGrids = [gridName, hGridName, visGridName]
    
    # Intialize Agent
    start = (10, 3)
    end = (3, 3)
    userAgent = Agent(start)

    # Actual juke variable, represents distance from finish to start
    juke = 0.9
    # Reformatting juke to display as a simple percentage from start to finish - more intuitive for users
    displayJuke = round((1-juke)*100)

    # Number of searches performed by the code
    searches = 3

    # Variables for Main Menu navigation
    selection = -1
    prompt = "Your selection: "
    
    # Loop main menu until user enters 7, which closes program
    while selection != 7:

        displayMainMenu(gridName, hGridName, visGridName, start, end, displayJuke, searches)

        selection = intInput(prompt, 1, 7)

        # Performs the pathfinding algorithm search
        if selection == 1:
            multiAStar(grid, hGrid, visGrid, start, end, juke, searches)
            hGrid = pd.read_csv(hGridPath) # Reset hGrid costs

        # Allows user to change grid files without restarting program
        elif selection == 2:
            newGrids = getGrids(allGrids)

            # Grid files update based on user inputs
            gridName = newGrids[0]
            gridPath = os.path.join(directory, gridName)
            grid = pd.read_csv(gridPath)
            hGridName = newGrids[1]
            hGridPath = os.path.join(directory, hGridName)
            hGrid = pd.read_csv(hGridPath)
            visGridName = newGrids[2]
            visGridPath = os.path.join(directory, visGridName)
            visGrid = pd.read_csv(visGridPath)

        # User can change start location
        elif selection == 3:
            numRows, numColumns = grid.shape
            start = getNewLocation("start", numRows, numColumns)

        # User can change end location
        elif selection == 4:
            numRows, numColumns = grid.shape
            end = getNewLocation("end", numRows, numColumns)

        # User can change location where algorithm begins juking (looking for alternative paths)
        elif selection == 5:
            juke = getJuke()
            displayJuke = round((1-juke)*100)

        # User can change number of alternative paths algorithm attempts to generate
        elif selection == 6:
            searches = getSearchAttempts()


    print("\nProgram has closed successfully\n")

########################################################################

if __name__ == "__main__":
    main()