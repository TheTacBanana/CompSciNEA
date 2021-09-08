import pygame, json, random
import perlinNoise, threading

class Tile(): # Class to store tile data in
    def __init__(self):
        self.tileHeight = -1

    def InitValues(self, tileType, height):
        self.tileType = tileType
        self.tileHeight = height

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

        self.interactableTileListTemp = []
        self.interactables = []


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

    def ConsoleOut(self): # Print grid of characters to console, representing the grid of tiles
        for y in range(0, self.MAP_SIZE):
            temp = ""
            for x in range(0, self.MAP_SIZE):
                temp += str(self.tileArray[x][y].tileHeight) + "/"
            print(temp)

    def GenerateTreeArea(self): # Uses perlin noise to generate the areas for trees to spawn in
        TSO = self.paramDictionary["TreeSeedOffset"]

        self.interactableTileListTemp = []
        self.interactables = []

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                temp = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + TSO, self.MAP_SEED + yCoord + TSO, 
                                                            self.paramDictionary["OctavesTrees"], self.paramDictionary["PersistenceTrees"])

                tileValue = Clamp(((self.tileArray[x][y].tileHeight / 2) + 0.5), 0.0, 1.0)

                if temp > self.paramDictionary["TreeHeight"] and tileValue > self.paramDictionary["Coast"] + self.paramDictionary["TreeBeachOffset"] and tileValue < self.paramDictionary["Grass"] - self.paramDictionary["TreeBeachOffset"]:
                    self.interactableTileListTemp.append([x, y])
        
        poissonCoords = self.PoissonDiscSampling(self.interactableTileListTemp, self.paramDictionary["PoissonRVal"], self.paramDictionary["PoissonKVal"])

        for coord in poissonCoords:
            self.interactables.append(InteractableObject("Tree", coord))

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

            for y in range(c[1] - r, c[1] + r + 1):
                for x in range(c[0] - r, c[0] + r + 1):
                    if x > 0 and x < self.MAP_SIZE and y > 0 and y < self.MAP_SIZE:
                        if treeMap[x][y] == 1:
                            flag == True

            if flag == False:
                i = 0
                treeMap[c[0]][c[1]] = 1
            else:   
                print(i, "first")
                i += 1
                print(i)
                flag = False

            c = listIn[random.randint(0, len(listIn) - 1)]

        treeList = []
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                if x > 0 and x < self.MAP_SIZE and y > 0 and y < self.MAP_SIZE:
                    if treeMap[x][y] == 1:
                        treeList.append([x,y])
        
        treeMap = None

        print(treeList)

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
            pass

        self.RenderMap()

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
                        colour = (18, 89, 144)
                    elif value < self.paramDictionary["Coast"]:
                        colour = (245, 234, 146)
                    elif value < self.paramDictionary["Grass"]:
                        colour = (26, 148, 49)
                    elif value < self.paramDictionary["TallGrass"]:
                        colour = (136, 140, 141)
                    
                    pygame.draw.rect(self.RenderedMap, colour, ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                            (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))

    def RenderInteractables(self, isList = True): # Renders list of interactables onto surface
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedInteractables = pygame.Surface((resolution, resolution))
        self.RenderedInteractables.set_colorkey((0,0,0))

        TTB = self.paramDictionary["TreeTileBorder"]

        if isList:
            for i in self.interactables:
                pygame.draw.rect(self.RenderedInteractables, (13, 92, 28), ((i.position[0] * self.TILE_WIDTH + TTB), 
                        (i.position[1] * self.TILE_WIDTH + TTB), self.TILE_WIDTH - (TTB * 2), self.TILE_WIDTH - (TTB * 2)))
        else:
            for y in range(0, self.MAP_SIZE):
                for x in range(0, self.MAP_SIZE):
                    value = self.interactableTempTileArray[x][y].tileHeight
                    value = (value / 2) + 0.5
                    value = Clamp(value, 0.0, 1.0)
                    
                    if value > 0.1:
                        pygame.draw.rect(self.RenderedInteractables, (13, 92, 28), ((x * self.TILE_WIDTH + TTB),
                                (y * self.TILE_WIDTH + TTB), self.TILE_WIDTH - (TTB * 2), self.TILE_WIDTH - (TTB * 2)))

    def DrawMap(self, window): # Blits the rendered frames onto the passed through window
        window.blit(self.RenderedMap, (0,0))
        window.blit(self.RenderedInteractables, (0,0))

def Clamp(val, low, high): # Simple function to clamp a value between two numbers - Used to make sure number doesnt go out of bounds
    return low if val < low else high if val > high else val