from worldClass import *
from newAgent import *
from enemy import *
from deepqlearning import *
import random, pygame, math

# Interface class between Main and Every other class
class Simulation():
    def __init__(self, params): # Constructor for Simulation
        self.paramDictionary = params

        self.worldMap = None
        self.network = None
        self.agent = None

        self.enemyList = []

        self.step = 0

# Step forward network methods
    def TimeStep(self): # Steps forward 1 cycle
        if not self.agent.alive: # Resets Sim if Agent is dead
            self.ResetOnDeath()

        self.network.TakeStep(self.agent, self.worldMap, self.enemyList) # Take step with Deep Q Network

        if self.paramDictionary["EnableEnemies"]: # If enemies enabled then update enemies
            self.UpdateEnemies()
            
        self.step += 1 

    def UpdateEnemies(self): # Updates Enemies
        self.enemyList = [x for x in self.enemyList if x is not None] # Clears None type from list

        return

        for i in range(len(self.enemyList)): # Commits each Enemies actions and sets to None if they died in that step
            self.enemyList[i].CommitAction(self.agent, self.worldMap)

            if not self.enemyList[i].alive: # Removes dead enemies from list
                self.enemyList[i] = None

        self.enemyList = [x for x in self.enemyList if x is not None] # Clears None type from list

# Creation and Initialisation Methods
    def InitiateSimulation(self): # Initialises Simulation
        self.CreateWorld()
        self.CreateAgent()

        self.CreateDeepQNetwork()

    def CreateWorld(self, seed = 0): # Creates new world with specified or random seed
        if seed == 0: seed = random.randint(0, 999999)
        
        if self.worldMap == None: # Creates a new world map if one does not exist - otherwise resets the seed
            self.worldMap = WorldMap(seed, self.paramDictionary)
        else:
            self.worldMap.MAP_SEED = seed

        if self.paramDictionary["GenerateThreaded"]: # Generates Terrain using 4 threads if specified
            self.worldMap.GenerateThreadedParent()
        else:
            self.worldMap.GenerateMap()

        self.worldMap.GenerateTreeArea() # Generates Tree Area

        self.worldMap.RenderMap() # Renders Map and Renders Interactables
        self.worldMap.RenderInteractables() 

        if self.paramDictionary["EnableEnemies"]: # Spawns Enemies if specified
            self.SpawnEnemies()

        print("Created New World, Seed: {}".format(seed))

    def CreateDeepQNetwork(self, layers = None): # Creates a Deep Q Network with the given Hyper Parameters
        if layers == None:
            layers = self.paramDictionary["DeepQLearningLayers"]

        if self.network == None: # Creates a Network if one doesnt already exist
            if self.paramDictionary["EnterValues"]:
                load = input("Load weights (Y/N): ")
                if load.upper() == "Y":
                    fName = input("State file name: ")

                    self.network = DoubleNeuralNet(layers, self.paramDictionary, load=True, loadName=fName)
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
        
        for count in range(n): # Spawns enemies for count
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

        if self.paramDictionary["EnableEnemies"]: # Spawns Enemies if specified
            self.SpawnEnemies()

# Render Methods
    def RenderToCanvas(self, window): # Render Content to Canvas
        TW = self.paramDictionary["TileWidth"]
        DS = self.paramDictionary["DebugScale"]

        if self.paramDictionary["Debug"]: # Renders debug info for Neural Network if specified
            for i in range(len(self.network.MainNetwork.layers)):
                for k in range(self.network.MainNetwork.layers[i].activations.order[0]):
                    value = self.network.MainNetwork.layers[i].activations.matrixVals[k][0]
                    newVal = (math.tanh(value) + 1) / 2
                    colourTuple = (255 * newVal, 255 * newVal, 255 * newVal)

                    try: # Exceps if colour value out of range
                        pygame.draw.rect(window, colourTuple, ((self.paramDictionary["WorldSize"] * TW + i * TW * DS), (k * TW * DS), (TW * DS), (TW * DS)))
                    except:
                        print(newVal)

        self.worldMap.DrawMap(window) # Draws Content to window 

        for i in range(len(self.enemyList)): # Draws enemies to window
            pygame.draw.rect(window, self.paramDictionary["ColourEnemy"], ((self.enemyList[i].location[0] * TW), (self.enemyList[i].location[1] * TW), TW, TW))

        # Draws Player to window
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
        file = open("Parameters\\{}.param".format(fname), "r") # Read range file
        paramRanges = json.loads(file.read()) # Load with json module
        file.close()

        for param in params: # Checks if parameter is specified in range file - If specified than check against given value to check within range
            if param in paramRanges:
                valRange = paramRanges[param]
                val = params[param]

                if valRange[1] == None: pass
                elif val > valRange[1]:
                    raise Exception("'{}' of value {}, has exceeded the range: {}-{}".format(param, val, valRange[0], valRange[1])) # Greater than specified range

                if valRange[1] == None: pass
                elif val < valRange[0]:
                    raise Exception("'{}' of value {}, has subceeded the range: {}-{}".format(param, val, valRange[0], valRange[1])) # Less than specified range

        print("Parameters within Specified Ranges")