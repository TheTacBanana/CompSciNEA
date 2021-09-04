import pygame, json, random
import perlinNoise, threading

class Tile():
    def __init__(self):
        self.tileHeight = -1

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

        self.time = 0
        
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
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, self.paramDictionary["Octaves"], self.paramDictionary["Persistence"])

        #self.time += (1 / self.MAP_SIZE)

    def ThreadedChild(self, x1, x2, y1, y2):
        for y in range(y1, y2):
            for x in range(x1, x2):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, self.paramDictionary["Octaves"], self.paramDictionary["Persistence"])

    def GenerateThreadedParent(self):
        threads = []

        halfMap = int(self.MAP_SIZE / 2)
        fullMap = self.MAP_SIZE

        threads.append(threading.Thread(target=self.ThreadedChild, args=(0, halfMap, 0, halfMap)))
        threads.append(threading.Thread(target=self.ThreadedChild, args=(halfMap, fullMap, 0, halfMap)))
        threads.append(threading.Thread(target=self.ThreadedChild, args=(0, halfMap, halfMap, fullMap)))
        threads.append(threading.Thread(target=self.ThreadedChild, args=(halfMap, fullMap, halfMap, fullMap)))
            
        for t in threads:
            t.start()

        while threading.activeCount() > 1:
            pass

        self.RenderMap()

        #print(threading.activeCount())


    def RenderMap(self):
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedMap = pygame.Surface((resolution, resolution))
        self.RenderedMap.set_colorkey((0,0,0))

        if self.paramDictionary["Grayscale"] == 1:
            for y in range(0, self.MAP_SIZE):
                for x in range(0, self.MAP_SIZE):
                    value = self.tileArray[x][y].tileHeight
                    value = (value / 2) + 0.5
                    value = Clamp(value, 0.0, 1.0)
                    
                    pygame.draw.rect(self.RenderedMap, (255 * value, 255 * value, 255 * value), ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                    (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))

        else:
            for y in range(0, self.MAP_SIZE):
                for x in range(0, self.MAP_SIZE):
                    value = self.tileArray[x][y].tileHeight
                    value = (value / 2) + 0.5
                    value = Clamp(value, 0.0, 1.0)
                    
                    colour = None

                    if value == 0:
                        colour = (0,0,0)
                    elif value < self.paramDictionary["Water"]:
                        colour = (18, 89, 144)
                    elif value < self.paramDictionary["Coast"]:
                        colour = (245, 234, 146)
                    elif value < self.paramDictionary["Grass"]:
                        colour = (26, 148, 49)
                    elif value < self.paramDictionary["TallGrass"]:
                        colour = (136, 140, 141)
                    
                    pygame.draw.rect(self.RenderedMap, colour, ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                    (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))


    def DrawMap(self, window):
        window.blit(self.RenderedMap, (0,0))

    
def Clamp(val, low, high):
    return low if val < low else high if val > high else val