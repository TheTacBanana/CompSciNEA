from worldClass import *
from random import shuffle
from matrix import Matrix

class Agent():
    def __init__(self, location, params):
        self.location = location
        self.paramDictionary = params

        self.inventory = {}

        self.explored = self.tileArray = [[Tile() for i in range(params["WorldSize"])] for j in range(params["WorldSize"])]

    def GetState(self, worldMap):
        world = worldMap.tileArray
        offset = self.paramDictionary["Offset"]

        temp = [[0 for i in range(self.location[0] - offset, self.location[0] + offset + 1)] for j in range(self.location[1] - offset, self.location[1] + offset + 1)]

        x1, y1 = 0, 0
        for y in range(self.location[0] - offset, self.location[0] + offset + 1):
            for x in range(self.location[1] - offset, self.location[1] + offset + 1):
                if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1:
                    temp[x1][y1] = world[x][y].tileType

                    for i in worldMap.interactables:
                        if i.position == [x,y]:
                            temp[x1][y1] = "T"
                x1 += 1
            x1 = 0
            y1 += 1

        #print(temp2)
        return temp

    def GetStateVector(self, worldMap): # Neural Network Input
        world = worldMap.tileArray
        offset = self.paramDictionary["DQLOffset"]

        sideLength = 2 * offset + 1
        temp = Matrix((sideLength * sideLength, 1))
        n = 0

        x1, y1 = 0, 0
        for y in range(self.location[0] - offset, self.location[0] + offset + 1):
            for x in range(self.location[1] - offset, self.location[1] + offset + 1):
                if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1:
                    flag = False
                    #print(n)
                    for i in worldMap.interactables:
                        if i.position == [x,y]:
                            flag = True
                            temp.matrixVals[n][0] = 5
                            n += 1

                    if flag == False:
                        temp.matrixVals[n][0] = world[x][y].tileType
                        n += 1

                x1 += 1
            x1 = 0
            y1 += 1
        return temp

    @staticmethod
    def SpawnPosition(worldMap):
        spawnList = []

        for y in range(0, worldMap.MAP_SIZE):
            for x in range(0, worldMap.MAP_SIZE):
                if worldMap.tileArray[x][y].tileType == 2:
                    spawnList.append([x, y])

        shuffle(spawnList)
        return spawnList[0]

    def Action(self, action, worldMap, maxQ = False):
        
        if action == 0:
            return self.Move(0, worldMap, maxQ)
        elif action == 1:
            return self.Move(1, worldMap, maxQ)
        elif action == 2:
            return self.Move(2, worldMap, maxQ)
        elif action == 3:
            return self.Move(3, worldMap, maxQ)
        elif action == 4:
            return self.PickupItem(worldMap, maxQ)

    def Move(self, direction, worldMap, maxQ): # 0 - Up 1 - Right 2 - Down 3 - Left
        if direction == 0 and worldMap.CheckIfOcean(self.location[0], self.location[1] - 1) != None:          #worldMap.tileArray[self.location[0]][self.location[1] - 1].tileType != 0:
            if not maxQ:
                self.location = [self.location[0], self.location[1] - 1]
            return self.paramDictionary["MoveReward"]
        elif direction == 1 and worldMap.CheckIfOcean(self.location[0] + 1, self.location[1]) != None: #worldMap.tileArray[self.location[0] + 1][self.location[1]].tileType != 0:
            if not maxQ:
                self.location = [self.location[0] + 1, self.location[1]]
            return self.paramDictionary["MoveReward"]
        elif direction == 2 and worldMap.CheckIfOcean(self.location[0], self.location[1] + 1) != None: #and worldMap.tileArray[self.location[0]][self.location[1] + 1].tileType != 0:
            if not maxQ:
                self.location = [self.location[0], self.location[1] + 1]
            return self.paramDictionary["MoveReward"]
        elif direction == 3 and worldMap.CheckIfOcean(self.location[0] - 1, self.location[1]) != None: #and worldMap.tileArray[self.location[0] - 1][self.location[1]].tileType != 0:
            if not maxQ:
                self.location = [self.location[0] - 1, self.location[1]]
            return self.paramDictionary["MoveReward"]
        else:
            return self.paramDictionary["TimeWasteReward"]

    def PickupItem(self, worldMap, maxQ):
        for i in worldMap.interactables:
            if i.position == self.location:
                #print("tree lol")
                return self.paramDictionary["TreeReward"]
        return self.paramDictionary["TimeWasteReward"]

# ---------------------------------------------------------------------------------------------------------------
    def NewMove(self, dir):
        pass

    def TakeAction(self, action, worldMap):
        maxQ = False
        if action == 0:
            return  self.Move(0, worldMap, maxQ)
        elif action == 1:
            return self.Move(1, worldMap, maxQ)
        elif action == 2:
            return self.Move(2, worldMap, maxQ)
        elif action == 3:
            return self.Move(3, worldMap, maxQ)
        elif action == 4:
            return self.PickupItem(worldMap, maxQ)

    def GetReward(self, action, worldMap):
        cumReward = 0
        #print(action)
        if action == 0 and worldMap.CheckIfOcean(self.location[0], self.location[1] - 1) != None:          #worldMap.tileArray[self.location[0]][self.location[1] - 1].tileType != 0:
            if self.explored[self.location[0]][self.location[1] - 1] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0]][self.location[1] - 1] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 1 and worldMap.CheckIfOcean(self.location[0] + 1, self.location[1]) != None: #worldMap.tileArray[self.location[0] + 1][self.location[1]].tileType != 0:
            if self.explored[self.location[0] + 1][self.location[1]] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0] + 1][self.location[1]] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 2 and worldMap.CheckIfOcean(self.location[0], self.location[1] + 1) != None: #and worldMap.tileArray[self.location[0]][self.location[1] + 1].tileType != 0:
            if self.explored[self.location[0]][self.location[1] + 1] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0]][self.location[1] + 1] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 3 and worldMap.CheckIfOcean(self.location[0] - 1, self.location[1]) != None: #and worldMap.tileArray[self.location[0] - 1][self.location[1]].tileType != 0:
            if self.explored[self.location[0] - 1][self.location[1]] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0] - 1][self.location[1]] = True
            cumReward += self.paramDictionary["MoveReward"]

        #elif action == 4 and worldMap.GetTile(self.location[0], self.location[1]).

        else:
            cumReward += self.paramDictionary["TimeWasteReward"]

        return cumReward

    def GetRewardWithVector(self, action, vector):
        cumReward = 0
        offset = self.paramDictionary["DQLOffset"] 
        sideLength = (offset * 2) + 1

        if action == 0 and vector.matrixVals[sideLength * 3 + offset][0] >= 1: # Move Up
            if self.explored[self.location[0]][self.location[1] - 1] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0]][self.location[1] - 1] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 1 and vector.matrixVals[sideLength * 4 + offset - 1][0] >= 1: # Move Right
            if self.explored[self.location[0] + 1][self.location[1]] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0] + 1][self.location[1]] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 2 and vector.matrixVals[sideLength * 4 + offset + 1][0] >= 1: # Move Down
            if self.explored[self.location[0]][self.location[1] + 1] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0]][self.location[1] + 1] = True
            cumReward += self.paramDictionary["MoveReward"]

        elif action == 3 and vector.matrixVals[sideLength * 5 + offset][0] >= 1: # Move Left
            if self.explored[self.location[0] - 1][self.location[1]] == False:
                cumReward += self.paramDictionary["ExploreReward"]
                self.explored[self.location[0] - 1][self.location[1]] = True
            cumReward += self.paramDictionary["MoveReward"]

        #elif action == 4 and worldMap.GetTile(self.location[0], self.location[1]).

        else:
            cumReward += self.paramDictionary["TimeWasteReward"]

        return cumReward