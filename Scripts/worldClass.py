import json, random, pygame, threading
import perlinNoise

# Class to store Individual Tile Data
class Tile(): 
    def __init__(self): # Initialise Tile object
        self.tileHeight = -1
        self.tileType = 0
        self.tileColour = (0,0,0)
        self.explored = False
        self.hasObject = False
        self.hasEnemy = False

    def InitValues(self, tileType, height, colour): # Set/Initialise Tile Vales
        self.tileType = tileType
        self.tileHeight = height
        self.tileColour = colour

    def AddObject(self, objectType, objectColour): # Adds an Object to the Tile Object
        self.hasObject = True
        self.objectType = objectType
        self.objectColour = objectColour
    
    def ClearObject(self): # Clears Object from the Tile Object
        self.hasObject = False
        self.objectType = ""
        self.objectColour = (0,0,0)

    def WriteEnemy(self): # Write Enemy to tile
        self.hasEnemy = True

    def __str__(self): # To String Overload
        if self.hasObject:
            return ("{},{}").format(self.tileType, self.objectType)
        else:
            return("{}").format(self.tileType)

# Class to store world terrain and object data
class WorldMap(): 
    def __init__(self, seed, params): # Initialise method for creating an instance of the world
        self.MAP_SIZE = params["WorldSize"]
        self.TILE_WIDTH = params["TileWidth"]
        self.MAP_SEED = seed
        self.TILE_BORDER = params["TileBorder"]

        self.tileArray = [[Tile() for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        self.paramDictionary = params

        self.time = 0

# Non Threaded Terrain Generation
    def GenerateMap(self): # Generates terrain - Not Threaded 
        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                xCoord = x / self.MAP_SIZE * self.paramDictionary["WorldScale"]
                yCoord = y / self.MAP_SIZE * self.paramDictionary["WorldScale"]

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, 
                                                            self.paramDictionary["OctavesTerrain"], self.paramDictionary["PersistenceTerrain"])

# Threaded Terrain Generation
    def GenerateThreadedParent(self): # Generates terrain using 4 threads
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

    def ThreadedChild(self, x1, x2, y1, y2): # Child Method to GenerateThreadedParent
        for y in range(y1, y2):
            for x in range(x1, x2):
                xCoord = (x / self.MAP_SIZE) * self.paramDictionary["WorldScale"]
                yCoord = (y / self.MAP_SIZE) * self.paramDictionary["WorldScale"]

                self.tileArray[x][y].tileHeight = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + self.time, self.MAP_SEED + yCoord + self.time, 
                                                            self.paramDictionary["OctavesTerrain"], self.paramDictionary["PersistenceTerrain"])

# Generate Tree Methods
    def GenerateTreeArea(self): # Uses perlin noise to generate the areas for trees to spawn in
        TSO = self.paramDictionary["TreeSeedOffset"]

        treeList = []

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                xCoord = x / self.MAP_SIZE
                yCoord = y / self.MAP_SIZE

                temp = perlinNoise.octaveNoise(self.MAP_SEED + xCoord + TSO, self.MAP_SEED + yCoord + TSO, 
                            self.paramDictionary["OctavesTrees"], self.paramDictionary["PersistenceTrees"])

                tileValue = self.Clamp(((self.tileArray[x][y].tileHeight / 2) + 0.5), 0.0, 1.0)

                if (temp > self.paramDictionary["TreeHeight"] and tileValue > self.paramDictionary["Coast"] + self.paramDictionary["TreeBeachOffset"] and 
                                                                    tileValue < self.paramDictionary["Grass"] - self.paramDictionary["TreeBeachOffset"]):
                    treeList.append([x, y]) 
        
        poissonArray = self.PoissonDiscSampling(treeList)

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                self.tileArray[x][y].ClearObject()

                if poissonArray[x][y] == True:
                    self.tileArray[x][y].AddObject(self.paramDictionary["TreeType"], self.paramDictionary["ColourTree"])

    def PoissonDiscSampling(self, pointList): # A tweaked version of poisson disc sampling in 2 dimensions
        k = self.paramDictionary["PoissonKVal"]

        pickedPoints = [[False for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        numPoints = len(pointList) - 1
        if numPoints <= 0: # Catches if no points
            return pickedPoints

        sampleNum = 0

        while sampleNum <= k:
            sample = pointList[random.randint(0, numPoints)]

            result = self.PoissonCheckPoint(sample, pickedPoints)
            if result == True:
                pickedPoints[sample[0]][sample[1]] = True
                sampleNum = 0
                continue
            else:
                sampleNum += 1
                continue

        return pickedPoints

    def PoissonCheckPoint(self, point, pickedPoints): # Checks Specific points around a point for objects
        if (1 <= point[0] and point[0] <= self.paramDictionary["WorldSize"] - 2 and 
                    1 <= point[1] and point[1] <= self.paramDictionary["WorldSize"] - 2):
            if pickedPoints[point[0]][point[1] - 1] == True: return False
            elif pickedPoints[point[0] + 1][point[1]] == True: return False
            elif pickedPoints[point[0]][point[1] + 1] == True: return False
            elif pickedPoints[point[0] - 1][point[1]] == True: return False
            elif pickedPoints[point[0]][point[1]] == True: return False
            else: return True

# Render Methods
    def RenderMap(self): # Renders terrain onto Pygame surface
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedMap = pygame.Surface((resolution, resolution))
        self.RenderedMap.set_colorkey((0,0,0))

        if self.paramDictionary["Grayscale"] == 1: # Renders in grayscale if needed
            for y in range(0, self.MAP_SIZE):
                for x in range(0, self.MAP_SIZE):
                    value = self.tileArray[x][y].tileHeight
                    value = (value / 2) + 0.5
                    value = self.Clamp(value, 0.0, 1.0)
                    
                    pygame.draw.rect(self.RenderedMap, (255 * value, 255 * value, 255 * value), ((x * self.TILE_WIDTH + self.TILE_BORDER), 
                            (y * self.TILE_WIDTH + self.TILE_BORDER), self.TILE_WIDTH - (self.TILE_BORDER * 2), self.TILE_WIDTH - (self.TILE_BORDER * 2)))

        else:                                      # Else renders in Colour
            for y in range(0, self.MAP_SIZE):
                for x in range(0, self.MAP_SIZE):
                    value = self.tileArray[x][y].tileHeight
                    value = (value / 2) + 0.5
                    value = self.Clamp(value, 0.0, 1.0)
                    
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

    def RenderInteractables(self): # Renders interactables onto pygame surface
        resolution = self.MAP_SIZE * self.TILE_WIDTH
        self.RenderedInteractables = pygame.Surface((resolution, resolution))
        self.RenderedInteractables.set_colorkey((0,0,0))

        ITB = self.paramDictionary["InteractableTileBorder"]

        for y in range(0, self.MAP_SIZE):
            for x in range(0, self.MAP_SIZE):
                if self.tileArray[x][y].hasObject == True:
                    tile = self.tileArray[x][y]
                    pygame.draw.rect(self.RenderedInteractables, tile.objectColour, ((x * self.TILE_WIDTH + ITB),
                            (y * self.TILE_WIDTH + ITB), self.TILE_WIDTH - (ITB * 2), self.TILE_WIDTH - (ITB * 2)))

    def DrawMap(self, window): # Blits the rendered frames onto the passed through window
        window.blit(self.RenderedMap, (0,0))
        self.RenderInteractables()
        window.blit(self.RenderedInteractables, (0,0))

    def RenderConsole(self):
        render = ""
        for y in range(0, self.MAP_SIZE):
            render += str([str(self.tileArray[i][y].tileType) for i in range(self.MAP_SIZE)]) + "\n"

        print(render)

# Miscellaneous Methods
    def Clamp(self, val, low, high): # Simple function to clamp a value between two numbers - Used to make sure number doesnt go out of bounds
        return low if val < low else high if val > high else val