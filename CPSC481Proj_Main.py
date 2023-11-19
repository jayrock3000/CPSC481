
class Agent:
    location = (0, 0)

    def __init__(self, X):
        self.location = X

    def setLoc(self, X):
        self.location = X

    def getLoc(self):
        return self.location 


def main():
    debug = True

    # Import Libraries
    import pandas as pd

    # Initialize Grid 
    #   Create dataframe to hold csv path cost grid
    grid = pd.read_csv(r"E:\School\Fullerton\2023_ Fall\CPSC 481\CPSC481 Project\CPSC481\grids - testGrid1.csv")
    #   Access grid values using grid.iat[0,0], grid.iat[0, 1], etc
    #   Access grid size using grid.shape, and individual dimensions with grid.shape[0] & grid.shape[1]

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
    tupac = Agent((0, 0))
    if debug == True:
        print("agent initialized with location ", end='')
        print(tupac.getLoc())


    print("\nProgram has closed successfully\n")


if __name__ == "__main__":
    main()