from worldClass import *
from random import shuffle
from matrix import Matrix

class Agent():
    def __init__(self, location, params):
        self.paramDictionary = params

        self.location = location

        self.alive = True

    @staticmethod
    def SpawnPosition(worldMap): # Returns a coord in which the Agent can spawn
        spawnList = []

        for y in range(0, worldMap.MAP_SIZE):
            for x in range(0, worldMap.MAP_SIZE):
                if worldMap.tileArray[x][y].tileType == 2:
                    spawnList.append([x, y])

        shuffle(spawnList)
        return spawnList[0]

# Methods for tile vectors
    def GetTileVector(self, worldMap): # Returns a Vector of Tile Datatype
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1
        tileVec = Matrix((sideLength * sideLength, 1))

        x1, y1, n = 0, 0, 0
        for y in range(self.location[0] - offset, self.location[0] + offset + 1): # Loop through Tiles in surrounding area
            for x in range(self.location[1] - offset, self.location[1] + offset + 1):
                tileVec.matrixVals[n][0] = worldMap.tileArray[x][y]
                
        return tileVec

    def TileVectorPostProcess(self, tileVec): # Returns 2 Vectors, 1 of tile types, 1 of grayscale values
        tileTypeVec = Matrix(tileVec.order)
        tileGrayscaleVec = Matrix(tileVec.order)

        for n in range(tileVec.order[0]):
            tileTypeVec[n][0] = tileVec[n][0].tileType

            tileGrayscaleVec[n][0] = self.ColourToGrayscale(tileVec[n][0].tileColour)

        return tileTypeVec, tileGrayscaleVec

    def ColourToGrayscale(self, colourTuple): # Converts colour value (255,255,255) to grayscale (0-1)
        grayscale = (0.299 * colourTuple[0] + 0.587 * colourTuple[1] + 0.114 * colourTuple[2]) / 255 
        return grayscale

# Action Methods
    def CommitAction(self, action, tileTypeVec, worldMap): # Commits the given Action
        if action == 0:
            self.Move(action, tileTypeVec, worldMap) # Move Up

        elif action == 1:
            self.Move(action, tileTypeVec, worldMap) # Move Right

        elif action == 2:
            self.Move(action, tileTypeVec, worldMap) # Move Down

        elif action == 3:
            self.Move(action, tileTypeVec, worldMap) # Move Left

        elif action == 4 and hasattr(tileTypeVec.matrixVals[(sideLength * offset) + offset][0], "objectType"):
            self.PickupItem(worldMap)

        elif action == 5:
            self.Attack(worldMap)

    def Move(self, direction, tileTypeVec, worldMap): # Moves agent in given Direction
        if action == 0: # Move Up
            self.location = [self.location[0], self.location[1] - 1]

        elif action == 1: # Move Right
            self.location = [self.location[0] + 1, self.location[1]]

        elif action == 2: # Move Down
            self.location = [self.location[0], self.location[1] + 1]

        elif action == 3: # Move Left
            self.location = [self.location[0] - 1, self.location[1]]

        if worldMap.tileArray[self.location[0]][self.location[1]].tileType == 0:
            self.alive == False

        if worldMap.tileArray[self.location[0]][self.location[1]].explored == False: 
            worldMap.tileArray[self.location[0]][self.location[1]].explored = True

    def PickupItem(self, worldMap): # Pickup Item in the same tile as Agent
        raise NotImplementedError

    def Attack(self): # Attacks in a given Area surrounding Agent
        raise NotImplementedError

# Reward Method
    def GetRewardVector(self, tileTypeVec):
        raise NotImplementedError