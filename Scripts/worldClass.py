import pygame, json, random

class Tile():
    def __init__(self):
        pass

    def InitValues(self, tileType, height):
        self.tileType = tileType
        self.tileHeight = height

class WorldMap():
    def __init__(self, size, tileWidth, seed):
        self.MAP_SIZE = size
        self.TILE_WIDTH = tileWidth
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

    def GetParameter(self, param):
        return self.paramDictionary[param]

    def ConsoleOut(self): # Print grid of characters to console, representing the grid of tiles
        for y in range(0, self.MAP_SIZE):
            temp = ""
            for x in range(0, self.MAP_SIZE):
                temp += "⬜"
            print(temp)

    def GenerateMap(self):
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                self.tileArray[x][y].tileHeight = random.randint(0, 1)

    def RenderMap(self):
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedMap = pygame.Surface((resolution, resolution))
        self.RenderedMap.set_colorkey((0,0,0))

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                value = self.tileArray[x][y].tileHeight
                pygame.draw.rect(self.RenderedMap, (255 * value, 255 * value, 255 * value), ((x * self.MAP_SIZE * self.TILE_WIDTH), (y * self.MAP_SIZE * self.TILE_WIDTH), self.TILE_WIDTH, self.TILE_WIDTH))
                pass

    def DrawMap(self, window):
        window.blit(self.RenderedMap, (0,0))