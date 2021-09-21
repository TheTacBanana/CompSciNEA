from worldClass import InteractableObject, Tile

class Agent():
    def __init__(self, location, params):
        self.location = location
        self.paramDictionary = params

        self.inventory = {}

    @staticmethod
    def SpawnPosition(worldMap):
        return [32,32]

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