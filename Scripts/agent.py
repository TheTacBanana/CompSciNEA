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

        print(temp)

        x1, y1 = 0, 0
        for y in range(self.location[0] - offset, self.location[0] + offset + 1):
            
            for x in range(self.location[1] - offset, self.location[1] + offset + 1):
                temp[x1][y1] = world[x][y].tileType
                x1 += 1
            x1 = 0
            y1 += 1

        return temp

    @staticmethod
    def SpawnPosition(worldMap):
        return [3,3]

    def Action(self, action, worldMap):
        if action == 0:
            self.Move(0, worldMap)
        elif action == 1:
            self.Move(0, worldMap)
        elif action == 2:
            self.Move(0, worldMap)
        elif action == 3:
            self.Move(0, worldMap)

    def Move(self, direction, worldMap): # 0 - Up 1 - Right 2 - Down 3 - Left
        if direction == 0:
            location = [location[0], location[1] - 1]
        elif direction == 1:
            location = [location[0] + 1, location[1]]
        elif direction == 2:
            location = [location[0], location[1] + 1]
        elif direction == 3:
            location = [location[0] - 1, location[1]]
        
    def PickupItem(self, interactableList):
        pass