import json, random
import perlinNoise, threading
import pygame

class Tile(): # Class to store tile data in
    def __init__(self):
        self.tileHeight = -1
        self.tileType = 0
        self.tileColour = (0,0,0)
        self.explored = False
        self.hasObject = False

    def InitValues(self, tileType, height, colour):
        self.tileType = tileType
        self.tileHeight = height
        self.tileColour = colour

    def AddObject(self, objectType, objectColour):
        self.hasObject = True
        self.objectType = objectType
        self.objectColour = objectColour

class InteractableObject(): # Class to store interactable data in
    def __init__(self, name, position):
        self.name = name
        self.position = position

class WorldMap():
    def __init__(self, seed, params): # Initialise method for creating an instance of the world
        # Constants
        self.MAP_SIZE = params["WorldSize"]
        self.TILE_WIDTH = params["TileWidth"]
        self.MAP_SEED = seed
        self.TILE_BORDER = params["TileBorder"]

        self.tileArray = [[Tile() for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        self.paramDictionary = params

        self.time = 0
        
    def GenerateTreeArea(self): # Uses perlin noise to generate the areas for trees to spawn in
        TSO = self.paramDictionary["TreeSeedOffset"]

        treeList = []

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                temp = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + TSO, self.MAP_SEED + yCoord + TSO, 
                                                            self.paramDictionary["OctavesTrees"], self.paramDictionary["PersistenceTrees"])

                tileValue = Clamp(((self.tileArray[x][y].tileHeight / 2) + 0.5), 0.0, 1.0)

                if (temp > self.paramDictionary["TreeHeight"] and tileValue > self.paramDictionary["Coast"] + self.paramDictionary["TreeBeachOffset"] and 
                                                                    tileValue < self.paramDictionary["Grass"] - self.paramDictionary["TreeBeachOffset"]):
                    treeList.append([x, y]) 
        
        poissonCoords = self.NewPoissonDiscSampling(treeList)

        #poissonCoords = self.ShuffledDiscSampling(self.interactableTileListTemp, self.paramDictionary["PoissonRVal"], self.paramDictionary["PoissonKVal"])

        for coord in poissonCoords:
            self.tileArray[coord[0]][coord[1]].AddObject(1, self.paramDictionary["ColourTree"])

    def NewPoissonDiscSampling(self, array):
        r = self.paramDictionary["PoissonRVal"]
        k = self.paramDictionary["PoissonKVal"]

        # https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf

    def ShuffledDiscSampling(self, listIn, r, k): # An algorithm for spacing objects in a given area - Inneficient and high complexity
        random.seed(self.MAP_SEED)
        random.shuffle(listIn)
        newList = []

        flag = False

        for coord in listIn:
            if len(newList) == 0:
                newList.append(coord)
            else:
                for newCoord in newList:
                    if self.NormalisedDistance(coord, newCoord) < r:
                        flag = True
                if flag:
                    flag = False
                    continue
                else:
                    newList.append(coord)

        return newList # List of coords with Trees

    def PoissonDiscSampling(self, listIn, r, k):
        if len(listIn) == 0:
            return []

        treeMap = [[0 for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        listCount = 0
        i = 0
        flag = False

        #print(len(listIn))

        # First point
        c = listIn[random.randint(0, len(listIn) - 1)]
        treeMap[c[0]][c[1]] = 1

        c = listIn[random.randint(0, len(listIn) - 1)]
        
        while i < k and listCount < len(listIn) - 1:
            listCount += 1

            for y in range(c[1] - r, c[1] + r ):
                for x in range(c[0] - r, c[0] + r):
                    if x > 0 and x < self.MAP_SIZE and y > 0 and y < self.MAP_SIZE:
                        if treeMap[x][y] == 1:
                            print(treeMap[x][y])
                            flag == True

            if flag == False:
                #print(i)
                i = 0
                treeMap[c[0]][c[1]] = 1
            else:   
                #print(i, "first")
                i += 1
                #print(i)
                flag = False

            c = listIn[random.randint(0, len(listIn) - 1)]

        treeList = []
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                if x > 0 and x < self.MAP_SIZE and y > 0 and y < self.MAP_SIZE:
                    if treeMap[x][y] == 1:
                        treeList.append([x,y])
        
        treeMap = None

        #print(treeList)

        return treeList       

    

    def NormalisedDistance(self, v1, v2): # Normalised distance between two points - used for Poisson Disc Sampling
        return ((v1[0]-v2[0]) ** 2 + (v1[1]-v2[1]) ** 2) ** 0.5

    def GenerateMap(self): # V1 - Not threaded
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, 
                                                            self.paramDictionary["OctavesTerrain"], self.paramDictionary["PersistenceTerrain"])

        #self.time += (1 / self.MAP_SIZE)

# Generate terrain using threaded methods
    def ThreadedChild(self, x1, x2, y1, y2): # V2 - Uses 4 threads to generate quicker
        for y in range(y1, y2):
            for x in range(x1, x2):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, 
                                                            self.paramDictionary["OctavesTerrain"], self.paramDictionary["PersistenceTerrain"])

    def GenerateThreadedParent(self): # Parent to Threaded Child method
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
            print("Threading")
            pass

        self.RenderMap()

    def CheckIfOcean(self,x,y):
        return True

    def RenderMap(self): # Renders terrain onto Pygame surface
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
                        colour = tuple(self.paramDictionary["ColourWater"])
                        self.tileArray[x][y].tileType = 0
                        self.tileArray[x][y].tileColour = colour
                    elif value < self.paramDictionary["Coast"]:
                        colour = tuple(self.paramDictionary["ColourCoast"])
                        self.tileArray[x][y].tileType = 1
                        self.tileArray[x][y].tileColour = colour
                    elif value < self.paramDictionary["Grass"]:
                        colour = tuple(self.paramDictionary["ColourGrass"])
                        self.tileArray[x][y].tileType = 2
                        self.tileArray[x][y].tileColour = colour
                    elif value < self.paramDictionary["Mountain"]:
                        colour = tuple(self.paramDictionary["ColourMountain"])
                        self.tileArray[x][y].tileType = 3
                        self.tileArray[x][y].tileColour = colour
                    
                    pygame.draw.rect(self.RenderedMap, colour, ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                            (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))

    def RenderInteractables(self, isList = True): # Renders list of interactables onto surface
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedInteractables = pygame.Surface((resolution, resolution))
        self.RenderedInteractables.set_colorkey((0,0,0))

        TTB = self.paramDictionary["TreeTileBorder"]

        if isList:
            for i in self.interactables:
                pygame.draw.rect(self.RenderedInteractables, tuple(self.paramDictionary["ColourTree"]), ((i.position[0] * self.TILE_WIDTH + TTB), 
                        (i.position[1] * self.TILE_WIDTH + TTB), self.TILE_WIDTH - (TTB * 2), self.TILE_WIDTH - (TTB * 2)))
        #else:
        #    for y in range(0, self.MAP_SIZE):
        #        for x in range(0, self.MAP_SIZE):
        #            value = self.interactableTempTileArray[x][y].tileHeight
        #            value = (value / 2) + 0.5
        #            value = Clamp(value, 0.0, 1.0)
        #            
        #            if value > 0.1:
        #                pygame.draw.rect(self.RenderedInteractables, (13, 92, 28), ((x * self.TILE_WIDTH + TTB),
        #                        (y * self.TILE_WIDTH + TTB), self.TILE_WIDTH - (TTB * 2), self.TILE_WIDTH - (TTB * 2)))

    def DrawMap(self, window): # Blits the rendered frames onto the passed through window
        window.blit(self.RenderedMap, (0,0))
        window.blit(self.RenderedInteractables, (0,0))

def Clamp(val, low, high): # Simple function to clamp a value between two numbers - Used to make sure number doesnt go out of bounds
    return low if val < low else high if val > high else val