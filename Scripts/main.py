import pygame
from worldClass import *
from qlearning import *
from deepqlearning import *
from agent import *
import math

#https://towardsdatascience.com/creating-deep-neural-networks-from-scratch-an-introduction-to-reinforcement-learning-6bba874019db
#http://www.briandolhansky.com/blog/2013/9/27/artificial-neural-networks-backpropagation-part-4

# Constant variables
worldSeed = 0
params = WorldMap.LoadParameters("Default")
worldMap = WorldMap(worldSeed, params)

headless = params["Headless"]
if not headless:
    worldResolution = worldMap.MAP_SIZE * worldMap.TILE_WIDTH
    window = pygame.display.set_mode((worldResolution + 100, worldResolution))

# Generates and renders the map to a single surface for optimisation
def Generate():
    global worldMap
    
    worldMap.MAP_SEED = random.randint(100000, 999999)
    
    worldMap.GenerateThreadedParent()
    worldMap.GenerateTreeArea()

    if not headless:
        worldMap.RenderMap()
        worldMap.RenderInteractables()

Generate()

#QNetwork = QLearning(params)
#QNetwork.CreateAgent(worldMap)
#agent = QNetwork.agent

DQNetwork = DoubleNeuralNet(params["DeepQLearningLayers"], params)
agent = Agent(Agent.SpawnPosition(worldMap), params)

TW = params["TileWidth"]
MS = params["QLearningMaxSteps"]

curCycle = 0
cycles = 10

#QNetwork.LoadQTable()

# Constant loop running
running = True
while running == True:
    if not headless:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN: # Key Down
                if event.key == pygame.K_F1:
                    Generate()

        #worldMap.RenderMap()
        
        #QNetwork.NextStep(worldMap)

        DQNetwork.TakeStep(agent, worldMap)
        worldMap.DrawMap(window)

        for i in range(len(DQNetwork.MainNetwork.layers)):
            for k in range(DQNetwork.MainNetwork.layers[i].outputVector.order[0]):
                value = DQNetwork.MainNetwork.layers[i].outputVector.matrixVals[k][0]
                value = math.tanh(value)
                #print((255/2) * value + (255/2))
                #print((255/2) * value + (255/2))

                pygame.draw.rect(window, (((255/2) * value) + (255/2), ((255/2) * value) + (255/2), 0), (((params["WorldSize"] * TW + i * TW * 2, (k * TW * 2), TW * 2, TW * 2))))

        #if QNetwork.step > MS:
        #    Generate()
        #    QNetwork.CreateAgent(worldMap)
        #    agent = QNetwork.agent
        #    curCycle += 1
        #    print(curCycle)

        #if curCycle > cycles:
        #    QNetwork.SaveQTable()
        #    running = False
        
        pygame.draw.rect(window, (233, 182, 14), ((agent.location[0] * TW), (agent.location[1] * TW), TW, TW))
        pygame.display.update()
    else:
        pass