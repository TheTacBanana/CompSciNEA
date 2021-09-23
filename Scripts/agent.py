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

    #def CalcReward(self, action, step):
    #    totalReward = 0
    #    if action >= 0 and action <= 3: 
    #        totalReward += self.paramDictionary["MoveReward"]

    #    if action == 4:
    #        totalReward += self.paramDictionary["TreeReward"]

    #    return totalReward

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