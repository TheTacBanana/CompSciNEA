from worldClass import *
from random import shuffle
from matrix import Matrix

class Agent():
    def __init__(self, location, params):
        self.paramDictionary = params

        self.location = location

        self.alive = True

        self.emptyInventory = {"Wood": 0, "Metal": 0}
        self.inventory = self.emptyInventory

# Methods for tile vectors
    def GetTileVector(self, worldMap, enemyList): # Returns a Vector of Tile Datatype
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1
        tileVec = Matrix((sideLength * sideLength, 1))

        blankOceanTile = Tile()
        blankOceanTile.InitValues(0, 0, self.paramDictionary["ColourWater"])

        n = 0
        for y in range(self.location[1] - offset, self.location[1] + offset + 1): # Loop through Tiles in surrounding area
            for x in range(self.location[0] - offset, self.location[0] + offset + 1):
                if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1:
                    tileVec.matrixVals[n][0] = worldMap.tileArray[x][y]
                else:
                    tileVec.matrixVals[n][0] = blankOceanTile
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
    def CommitAction(self, action, tileObjVec, worldMap): # Commits the given Action
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1

        tileTypeVec = self.TileVectorPostProcess(tileObjVec)
        if action == 0:
            self.Move(action, worldMap) # Move Up

        elif action == 1:
            self.Move(action, worldMap) # Move Right

        elif action == 2:
            self.Move(action, worldMap) # Move Down

        elif action == 3:
            self.Move(action, worldMap) # Move Left

        elif action == 4 and tileObjVec.matrixVals[(sideLength * offset) + offset][0].hasObject == True:
            self.PickupItem(worldMap)

        elif action == 5:
            self.Attack(worldMap)

    def Move(self, direction, worldMap): # Moves agent in given Direction
        if direction == 0: self.location = [self.location[0], self.location[1] - 1] # Move Up
        elif direction == 1: self.location = [self.location[0] + 1, self.location[1]] # Move Right
        elif direction == 2: self.location = [self.location[0], self.location[1] + 1] # Move Down
        elif direction == 3: self.location = [self.location[0] - 1, self.location[1]] # Move Left
           
        self.alive = self.CheckIfValidStandTile(self.location, worldMap)
        if not self.alive: return

        if worldMap.tileArray[self.location[0]][self.location[1]].explored == False: # Checks if tile is explored or not
            worldMap.tileArray[self.location[0]][self.location[1]].explored = True

    def CheckIfValidStandTile(self, location, worldMap): # Checks if tile will murder the agent
        x = location[0]
        y = location[1]
        if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1: pass
        else: 
            return False

        if worldMap.tileArray[x][y].tileType == 0: # Checks if tile is water
            return False

        return True

    def PickupItem(self, worldMap): # Pickup Item in the same tile as Agent
        if worldMap.tileArray[self.location[0]][self.location[1]].hasObject:
            self.inventory[worldMap.tileArray[self.location[0]][self.location[1]].objectType] += 1

            worldMap.tileArray[self.location[0]][self.location[1]].ClearObject()

    def Attack(self): # Attacks in a given Area surrounding Agent
        raise NotImplementedError

# Reward Method
    def GetReward(self, action, tileObjVec):
        offset = self.paramDictionary["DQLOffset"]
        sideLength = 2 * offset + 1

        cumReward = 0

        if action == 0: # Move Up
            tile = tileObjVec.matrixVals[(sideLength * (offset - 1)) + offset][0]
            cumReward += self.MoveReward(tile)
            
        elif action == 1: # Move Right
            tile = tileObjVec.matrixVals[(sideLength * offset) + offset + 1][0]
            cumReward += self.MoveReward(tile) 

        elif action == 2: # Move Down
            tile = tileObjVec.matrixVals[(sideLength * (offset + 1)) + offset][0]
            cumReward += self.MoveReward(tile) 

        elif action == 3: # Move Left
            tile = tileObjVec.matrixVals[(sideLength * offset) + offset - 1][0]
            cumReward += self.MoveReward(tile) 

        elif action == 4: # Pickup Item
            if tileObjVec.matrixVals[(sideLength * offset) + offset][0].hasObject:
                cumReward += self.paramDictionary["CollectItemReward"]

        elif action == 5:
            raise NotImplementedError

        return cumReward

    def MoveReward(self, tileObj): # Stops repeating the same code 4 times - Gets Reward given Agent moving into a tile
        #print(tile)
        reward = 0 
        if tileObj.tileType == 0:
            reward += self.paramDictionary["DeathReward"]
        else:
            if tileObj.explored == False:
                reward += self.paramDictionary["ExploreReward"]
            reward += self.paramDictionary["MoveReward"]
        return reward
            
    def GetRewardVector(self, tileObjVec, outputs): # Returns Vector of Reward Values Per action
        returnVec = Matrix((outputs, 1))

        for i in range(outputs):
            returnVec.matrixVals[i][0] = self.GetReward(i, tileObjVec)

        return returnVec

    def MaxQ(self, rewardVec):
        return max([rewardVec.matrixVals[i][0] for i in range(rewardVec.order[0])])

# Miscellaneous Methods
    def Reset(self, worldMap):
        self.inventory = self.emptyInventory

        self.alive = True

        self.location = Agent.SpawnPosition(worldMap)

    @staticmethod
    def SpawnPosition(worldMap): # Returns a coord in which the Agent can spawn
        spawnList = []

        for y in range(0, worldMap.MAP_SIZE):
            for x in range(0, worldMap.MAP_SIZE):
                if worldMap.tileArray[x][y].tileType == 2:
                    spawnList.append([x, y])

        shuffle(spawnList)
        return spawnList[0]