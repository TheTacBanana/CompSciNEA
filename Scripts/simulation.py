from worldClass import *
from newAgent import *
from enemy import *
from qlearning import *
from deepqlearning import *
import random, pygame, math

# Interface class between Main and Every other class
class Simulation(): 
    def __init__(self, networkType, params): # Creates an instance of Simulation
        self.paramDictionary = params

        self.networkType = networkType

        self.worldMap = None
        self.network = None
        self.agent = None

        self.enemyList = []

        self.step = 0

# Step forward network methods
    def TimeStep(self): # Steps forward 1 cycle
        if self.networkType == 0: # QLearning Network Step
            raise NotImplementedError

        elif self.networkType == 1: # Deep QLearning Network Step
            if not self.agent.alive:
                self.ResetOnDeath()

            self.network.TakeStep(self.agent, self.worldMap, self.enemyList)

            if self.paramDictionary["EnableEnemies"]:
                self.UpdateEnemies()

        self.step += 1

    def UpdateEnemies(self): # Updates Enemies
        self.enemyList = [x for x in self.enemyList if x is not None]

        for i in range(len(self.enemyList)):
            self.enemyList[i].CommitAction(self.agent, self.worldMap)

            if not self.enemyList[i].alive:
                self.enemyList[i] = None

        self.enemyList = [x for x in self.enemyList if x is not None]
        

# Creation and Initialisation Methods
    def InitiateSimulation(self): # Initialises Simulation
        self.CreateWorld()
        self.CreateAgent()

        if self.networkType == 0:
            self.CreateQNetwork()
        elif self.networkType == 1: 
            self.CreateDeepQNetwork()


    def CreateWorld(self, seed = 0): # Creates new world with specified or random seed
        if seed == 0: seed = random.randint(0, 999999)
        
        if self.worldMap == None:
            self.worldMap = WorldMap(seed, self.paramDictionary)
        else:
            self.worldMap.MAP_SEED = seed

        if self.paramDictionary["GenerateThreaded"]:
            self.worldMap.GenerateThreadedParent()
        else:
            self.worldMap.GenerateMap()

        self.worldMap.GenerateTreeArea() 

        self.worldMap.RenderMap()
        self.worldMap.RenderInteractables()

        if self.paramDictionary["EnableEnemies"]:
            self.SpawnEnemies()

        print("Created New World, Seed: {}".format(seed))

    def CreateQNetwork(self): # Creates a Q Network with the given Hyper Parameters
        raise NotImplementedError

    def CreateDeepQNetwork(self, layers = None): # Creates a Deep Q Network with the given Hyper Parameters
        if layers == None:
            layers = self.paramDictionary["DeepQLearningLayers"]

        if self.network == None: # Creates a Network if one doesnt already exist
            if self.paramDictionary["EnterValues"]:
                load = input("Load weights (Y/N): ")
                if load.upper() == "Y":
                    fNames = []
                    fNames.append(input("Main Network file name: "))
                    fNames.append(input("Target Network file name: "))

                    self.network = DoubleNeuralNet(layers, self.paramDictionary, load=True, loadNames=fNames)
                else:
                    self.network = DoubleNeuralNet(layers, self.paramDictionary)
            else:
                self.network = DoubleNeuralNet(layers, self.paramDictionary)

    def CreateAgent(self): # Creates an agent / Resets existing agent
        if self.agent == None:
            self.agent = Agent(Agent.SpawnPosition(self.worldMap), self.paramDictionary)
        else:
            self.agent.Reset(self.worldMap)

    def SpawnEnemies(self, n = 0): # Spawns <= n enemies on call
        if n == 0: n = self.paramDictionary["StartEnemyCount"]
        
        for i in range(n):
            spawnLoc = Enemy.SpawnPosition(self.worldMap, self.enemyList)
            if spawnLoc == None:
                continue
            else:
                tempEnemy = Enemy(spawnLoc, self.paramDictionary)
                self.enemyList.append(tempEnemy)

    def ResetOnDeath(self): # Resets Simulation if Agent Dies
        self.CreateWorld()
        self.CreateAgent()
        self.enemyList = []
        self.SpawnEnemies()
        self.step = 0

# Render Methods
    def RenderToCanvas(self, window, debug): # Render Content to Canvas
        TW = self.paramDictionary["TileWidth"]
        MS = self.paramDictionary["QLearningMaxSteps"]
        DS = self.paramDictionary["DebugScale"]

        if debug == True:
            for i in range(len(self.network.MainNetwork.layers)):
                for k in range(self.network.MainNetwork.layers[i].outputVector.order[0]):
                    value = self.network.MainNetwork.layers[i].outputVector.matrixVals[k][0]
                    newVal = (math.tanh(value) + 1) / 2
                    colourTuple = (255 * newVal, 255 * newVal, 255 * newVal)

                    pygame.draw.rect(window, colourTuple, ((self.paramDictionary["WorldSize"] * TW + i * TW * DS), (k * TW * DS), (TW * DS), (TW * DS)))

        self.worldMap.DrawMap(window)

        for i in range(len(self.enemyList)):
            pygame.draw.rect(window, self.paramDictionary["ColourEnemy"], ((self.enemyList[i].location[0] * TW), (self.enemyList[i].location[1] * TW), TW, TW))

        pygame.draw.rect(window, self.paramDictionary["ColourPlayer"], ((self.agent.location[0] * TW), (self.agent.location[1] * TW), TW, TW))

# Miscellaneous Methods
    @staticmethod
    def LoadParameters(fname): # Load Parameters from file and store them in a dictionary
        file = open("Parameters\\{}.param".format(fname), "r")
        params = json.loads(file.read())
        file.close()
        return params

    @staticmethod
    def CheckParameters(params, fname): # Checks every parameter against the range.parm file
        file = open("Parameters\\{}.param".format(fname), "r")
        paramRanges = json.loads(file.read())
        file.close()

        for param in params:
            if param in paramRanges:
                valRange = paramRanges[param]
                val = params[param]

                if valRange[1] == None: pass
                elif val > valRange[1]:
                    raise Exception("'{}' of value {}, has exceeded the range: {}-{}".format(param, val, valRange[0], valRange[1]))

                if valRange[1] == None: pass
                elif val < valRange[0]:
                    raise Exception("'{}' of value {}, has subceeded the range: {}-{}".format(param, val, valRange[0], valRange[1]))
        print("Parameters within Specified Ranges")