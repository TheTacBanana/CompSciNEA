import pygame, json, random
import perlinNoise

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

        self.tileArray = [[Tile() for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        self.paramDictionary = params
        
    @staticmethod
    def LoadParameters(fname): # Load Parameters from file and store them in a dictionary
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
                #self.tileArray[x][y].tileHeight = round(random.random(), 1)

                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE
                frequency = 16

                self.tileArray[x][y].tileHeight = perlinNoise.Noise(xCoord * frequency, yCoord * frequency)

    def RenderMap(self):
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedMap = pygame.Surface((resolution, resolution))
        self.RenderedMap.set_colorkey((0,0,0))

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                value = self.tileArray[x][y].tileHeight
                value = (value / 2) + 0.5
                value = Clamp(value, 0.0, 1.0)
                #print(value, x * self.MAP_SIZE * self.TILE_WIDTH, y * self.MAP_SIZE * self.TILE_WIDTH)
                pygame.draw.rect(self.RenderedMap, (255 * value, 255 * value, 255 * value), ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))
                pass

    def DrawMap(self, window):
        window.blit(self.RenderedMap, (0,0))

    
def Clamp(val, low, high):
    return low if val < low else high if val > high else val