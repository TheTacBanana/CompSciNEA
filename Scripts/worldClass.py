import pygame, json

class Tile():
    def __init__(self):
        pass

    def InitValues(self, tileType, height):
        self.tileType = tileType
        self.tileHeight = height

class WorldMap():
    def __init__(self, size, seed):
        self.MAP_SIZE = size
        self.MAP_SEED = seed

        self.tileArray = [[Tile() for i in range(size)] for j in range(size)]

        self.paramDictionary = self.LoadParameters("Default.param")
        
    def LoadParameters(self, fname): # Load Parameters from file and store them in a dictionary
        file = open("Parameters\\{}".format(fname), "r")
        params = json.loads(file.read())
        file.close()
        return params

    def GetTile(self, xpos, ypos): # Return tile at specified position
        return self.tileArray[xpos][ypos]

    def ConsoleOut(self): # Print grid of characters to console, representing the grid of tiles
        for y in range(0, self.MAP_SIZE):
            temp = ""
            for x in range(0, self.MAP_SIZE):
                temp += "⬜"
            print(temp)