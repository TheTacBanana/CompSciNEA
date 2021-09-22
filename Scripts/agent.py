from worldClass import *

class Agent():
    def __init__(self, location, params):
        self.location = location
        self.paramDictionary = params

        self.inventory = {}

    def GetState(self, worldMap):
        world = worldMap.tileArray
        offset = self.paramDictionary["Offset"]

        temp = [[0 for i in range(self.location[0] - offset, self.location[0] + offset + 1)] for j in range(self.location[1] - offset, self.location[1] + offset + 1)]

        #print(temp)

        x1, y1 = 0, 0
        for y in range(self.location[0] - offset, self.location[0] + offset + 1):
            
            for x in range(self.location[1] - offset, self.location[1] + offset + 1):
                if 0 <= x and x <= self.paramDictionary["WorldSize"] - 1 and 0 <= y and y <= self.paramDictionary["WorldSize"] - 1:
                    temp[x1][y1] = world[x][y].tileType
                x1 += 1
            x1 = 0
            y1 += 1

        return temp

    @staticmethod
    def SpawnPosition(worldMap):
        return [64,64]

    def CalcReward(self, action, step):
        totalReward = 0
        if action >= 0 and action <= 3: 
            totalReward += self.paramDictionary["MoveReward"]

        if action == 4:
            totalReward += self.paramDictionary["TreeReward"]

        return totalReward

    def Action(self, action, worldMap):
        if action == 0:
            self.Move(0, worldMap)
        elif action == 1:
            self.Move(1, worldMap)
        elif action == 2:
            self.Move(2, worldMap)
        elif action == 3:
            self.Move(3, worldMap)
        elif action == 4:
            self.PickupItem(worldMap.interactables)

    def Move(self, direction, worldMap): # 0 - Up 1 - Right 2 - Down 3 - Left
        if direction == 0 and worldMap.CheckIfOcean(self.location[0], self.location[1] - 1) != None:          #worldMap.tileArray[self.location[0]][self.location[1] - 1].tileType != 0:
            self.location = [self.location[0], self.location[1] - 1]

        elif direction == 1 and worldMap.CheckIfOcean(self.location[0] + 1, self.location[1]) != None: #worldMap.tileArray[self.location[0] + 1][self.location[1]].tileType != 0:
            self.location = [self.location[0] + 1, self.location[1]]

        elif direction == 2 and worldMap.CheckIfOcean(self.location[0], self.location[1] + 1) != None: #and worldMap.tileArray[self.location[0]][self.location[1] + 1].tileType != 0:
            self.location = [self.location[0], self.location[1] + 1]

        elif direction == 3 and worldMap.CheckIfOcean(self.location[0] - 1, self.location[1]) != None: #and worldMap.tileArray[self.location[0] - 1][self.location[1]].tileType != 0:
            self.location = [self.location[0] - 1, self.location[1]]

        
    def PickupItem(self, interactableList):
        pass
        #print("pickup lol")