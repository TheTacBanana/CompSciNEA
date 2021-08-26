import pygame, json, random

class Tile():
    def __init__(self):
        pass

    def InitValues(self, tileType, height):
        self.tileType = tileType
        self.tileHeight = height

class WorldMap():
    def __init__(self, seed, params):
        self.MAP_SIZE = params["WorldSize"]
        self.TILE_WIDTH = params["TileWidth"]
        self.MAP_SEED = seed
        self.TILE_BORDER = params["TileBorder"]

        self.tileArray = [[Tile() for i in range(size)] for j in range(size)]

        self.paramDictionary = params
        
    @staticmethod
    def LoadParameters(self, fname): # Load Parameters from file and store them in a dictionary
        file = open("Parameters\\{}.param".format(fname), "r")
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
                temp += str(self.tileArray[x][y].tileHeight) + "/"
            print(temp)

    def GenerateMap(self):
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                self.tileArray[x][y].tileHeight = round(random.random(), 1)

    def RenderMap(self):
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedMap = pygame.Surface((resolution, resolution))
        self.RenderedMap.set_colorkey((0,0,0))

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                value = self.tileArray[x][y].tileHeight
                #print(value, x * self.MAP_SIZE * self.TILE_WIDTH, y * self.MAP_SIZE * self.TILE_WIDTH)
                pygame.draw.rect(self.RenderedMap, (255 * value, 255 * value, 255 * value), ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))
                pass

    def DrawMap(self, window):
        window.blit(self.RenderedMap, (0,0))