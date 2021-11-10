from worldClass import *
from qlearning import *
from deepqlearning import *
from agent import *
import random
import pygame

class Simulation():
    def __init__(self, networkType, params):
        self.paramsDictionary = params

        self.networkType = networkType

        self.worldMap = None
        self.network = None
        self.agent = None

        self.step = 0

# Creation and Initialisation Methods
    def InitiateSimulation(self):
        CreateWorld()
        CreateAgent()

        if self.networkType == 0:
            CreateQNetwork()
        elif self.networkType == 1: 
            CreateDeepQNetwork()

    def CreateWorld(self, seed = random.randinit()):
        if self.worldMap == None:
            self.worldMap = WorldMap(seed, self.paramDictionary)
        else:
            self.worldMap.MAP_SEED = seed

        worldMap.GenerateThreadedParent()
        worldMap.GenerateTreeArea()

        worldMap.RenderMap()
        worldMap.RenderInteractables()

        print("Created New World, Seed: {}".format(seed))

    def CreateQNetwork(self):
        raise NotImplementedError

    def CreateDeepQNetwork(self, layers = None):
        if layers == None:
            layers = params["DeepQLearningLayers"]

        if self.network == None: # Creates a Network if one doesnt already exist
            self.network = DoubleNeuralNet(layers, self.paramDictionary)
        else:                    # Resets the existing network
            raise NotImplementedError

    def CreateAgent(self):
        if self.agent == None:
            self.agent = Agent(agent.SpawnPosition(self.worldMap), self.paramDictionary)
        else:
            self.agent.location = agent.SpawnPosition(self.worldMap)

# Step forward network methods
    def TimeStep(self):
        if self.networkType == 0: # QLearning Network Step
            raise NotImplementedError

        elif self.networkType == 1: # Deep QLearning Network Step
            self.network.TakeStep(self.agent, self.worldMap)

# Compile Drawn Layers
    def GetRenderedLayers(self):
        raise NotImplementedError
        
    def GetRenderedLayersAndDebug(self):
        raise NotImplementedError