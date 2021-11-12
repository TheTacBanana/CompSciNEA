from worldClass import *
from newAgent import *
from qlearning import *
from deepqlearning import *
import random
import pygame
import math

class Simulation():
    def __init__(self, networkType, params):
        self.paramDictionary = params

        self.networkType = networkType

        self.worldMap = None
        self.network = None
        self.agent = None

        self.enemies = []

        self.step = 0

# Step forward network methods
    def TimeStep(self):
        if self.networkType == 0: # QLearning Network Step
            raise NotImplementedError

        elif self.networkType == 1: # Deep QLearning Network Step
            self.network.TakeStep(self.agent, self.worldMap)

            if not self.agent.alive:
                raise NotImplementedError

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

        self.worldMap.GenerateThreadedParent()
        self.worldMap.GenerateTreeArea() 

        self.worldMap.RenderMap()
        self.worldMap.RenderInteractables()

        self.CreateAgent()

        print("Created New World, Seed: {}".format(seed))

    def CreateQNetwork(self):
        raise NotImplementedError

    def CreateDeepQNetwork(self, layers = None): # Creates a Deep Q Network with the given Hyper Parameters
        if layers == None:
            layers = self.paramDictionary["DeepQLearningLayers"]

        if self.network == None: # Creates a Network if one doesnt already exist
            self.network = DoubleNeuralNet(layers, self.paramDictionary)
        else:                    # Resets the existing network
            raise NotImplementedError

    def CreateAgent(self): # Creates an agent / Resets existing agent
        if self.agent == None:
            self.agent = Agent(Agent.SpawnPosition(self.worldMap), self.paramDictionary)
        else:
            self.agent.location = Agent.SpawnPosition(self.worldMap)

# Render Methods
    def RenderToCanvas(self, window, Debug = False): # Render Content to Canvas
        TW = self.paramDictionary["TileWidth"]
        MS = self.paramDictionary["QLearningMaxSteps"]

        if Debug == True:
            for i in range(len(self.network.MainNetwork.layers)):
                for k in range(self.network.MainNetwork.layers[i].outputVector.order[0]):
                    value = self.network.MainNetwork.layers[i].outputVector.matrixVals[k][0]
                    newVal = (math.tanh(value) + 1) / 2
                    colourTuple = (255 * newVal, 255 * newVal, 255 * newVal)

                    pygame.draw.rect(window, colourTuple, ((self.paramDictionary["WorldSize"] * TW + i * TW * 2), (k * TW * 2), (TW * 2), (TW * 2)))

        self.worldMap.DrawMap(window)
        pygame.draw.rect(window, (233, 182, 14), ((self.agent.location[0] * TW), (self.agent.location[1] * TW), TW, TW))

# Miscellaneous Methods
    @staticmethod
    def LoadParameters(fname): # Load Parameters from file and store them in a dictionary
        file = open("Parameters\\{}.param".format(fname), "r")
        params = json.loads(file.read())
        file.close()
        return params

    @staticmethod
    def CheckParameters(params, fname):
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