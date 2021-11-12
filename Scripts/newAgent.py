from worldClass import *
from random import shuffle
from matrix import Matrix

class Agent():
    def __init__(self, location, params):
        self.paramDictionary = params

        self.location = location

        self.alive = True

        self.inventory = {"Wood": 0}

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
                if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1:
                    tileVec.matrixVals[n][0] = worldMap.tileArray[x][y]
                    n += 1
                
        return tileVec

    def TileVectorPostProcess(self, tileVec): # Returns 2 Vectors, 1 of tile types, 1 of grayscale values
        tileTypeVec = Matrix(tileVec.order)
        tileGrayscaleVec = Matrix(tileVec.order)

        for n in range(tileVec.order[0]):
            tileTypeVec.matrixVals[n][0] = tileVec.matrixVals[n][0].tileType

            tileGrayscaleVec.matrixVals[n][0] = self.ColourToGrayscale(tileVec.matrixVals[n][0].tileColour)

        return tileTypeVec, tileGrayscaleVec

    def ColourToGrayscale(self, colourTuple): # Converts colour value (255,255,255) to grayscale (0-1)
        grayscale = (0.299 * colourTuple[0] + 0.587 * colourTuple[1] + 0.114 * colourTuple[2]) / 255 
        return grayscale

# Action Methods
    def CommitAction(self, action, tileTypeVec, worldMap): # Commits the given Action
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1

        if action == 0:
            self.Move(action, tileTypeVec, worldMap) # Move Up

        elif action == 1:
            self.Move(action, tileTypeVec, worldMap) # Move Right

        elif action == 2:
            self.Move(action, tileTypeVec, worldMap) # Move Down

        elif action == 3:
            self.Move(action, tileTypeVec, worldMap) # Move Left

        elif action == 4 and tileTypeVec.matrixVals[(sideLength * offset) + offset][0].hasObject == True:
            self.PickupItem(worldMap)

        elif action == 5:
            self.Attack(worldMap)

    def Move(self, direction, tileTypeVec, worldMap): # Moves agent in given Direction
        if direction == 0: # Move Up
            self.location = [self.location[0], self.location[1] - 1]

        elif direction == 1: # Move Right
            self.location = [self.location[0] + 1, self.location[1]]

        elif direction == 2: # Move Down
            self.location = [self.location[0], self.location[1] + 1]

        elif direction == 3: # Move Left
            self.location = [self.location[0] - 1, self.location[1]]

        if worldMap.tileArray[self.location[0]][self.location[1]].tileType == 0: # Checks if tile is water
            self.alive == False

        if worldMap.tileArray[self.location[0]][self.location[1]].explored == False: # Checks if tile is explored or not
            worldMap.tileArray[self.location[0]][self.location[1]].explored = True

    def PickupItem(self, worldMap): # Pickup Item in the same tile as Agent
        if worldMap.tileArray[self.location[0]][self.location[1]].hasObject:
            self.inventory[worldMap.tileArray[self.location[0]][self.location[1]]] += 1

            worldMap.tileArray[self.location[0]][self.location[1]].ClearObject()

    def Attack(self): # Attacks in a given Area surrounding Agent
        raise NotImplementedError

# Reward Method
    def GetReward(self, action, tileTypeVec):
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1

        cumReward = 0

        if action == 0: # Move Up
            tile = tileTypeVec.matrixVals[(sideLength * (offset - 1)) + offset][0]
            cumReward += self.MoveReward(tile)
            
        elif action == 1: # Move Right
            tile = tileTypeVec.matrixVals[(sideLength * offset) + offset + 1][0]
            cumReward += self.MoveReward(tile) 

        elif action == 2: # Move Down
            tile = tileTypeVec.matrixVals[(sideLength * (offset + 1)) + offset][0]
            cumReward += self.MoveReward(tile) 

        elif action == 3: # Move Left
            tile = tileTypeVec.matrixVals[(sideLength * offset) + offset - 1][0]
            cumReward += self.MoveReward(tile) 

        elif action == 4: # Pickup Item
            raise NotImplementedError

        elif action == 5:
            raise NotImplementedError

        return cumReward

    def MoveReward(self, tile): # Stops repeating the same code 4 times - Gets Reward given Agent moving into a tile
        reward = 0 
        if tile.tileType == 0:
            reward += self.paramDictionary["DeathReward"]
        else:
            if tile.explored == False:
                reward += self.paramDictionary["ExploreReward"]
            reward += self.paramDictionary["MoveReward"]
        return reward
            
    def GetRewardVector(self, tileTypeVec, outputs): # Returns Vector of Reward Values Per action
        returnVec = Matrix((outputs, 1))

        for i in range(outputs):
            returnVec.matrixVals[i][0] = self.GetReward(i, tileTypeVec)

        return returnVec