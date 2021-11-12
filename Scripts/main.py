import pygame
from simulation import *

params = Simulation.LoadParameters("Default")
Simulation.CheckParameters(params, "Range")

gameSim = Simulation(1, params)
gameSim.InitiateSimulation()

worldResolution = params["WorldSize"] * params["TileWidth"]
if params["Debug"]: debugOffset = (len(params["DeepQLearningLayers"] * params["TileWidth"] * 2))
else: debugOffset = 0
window = pygame.display.set_mode((worldResolution + debugOffset, worldResolution))

# Constant loop running
running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: # Key Down
            if event.key == pygame.K_F1:
                gameSim.CreateWorld()

    gameSim.TimeStep()

    gameSim.RenderToCanvas(window, params["Debug"])  

    pygame.display.update()

#TW = params["TileWidth"]
#MS = params["QLearningMaxSteps"]

#for i in range(len(DQNetwork.MainNetwork.layers)):
#    for k in range(DQNetwork.MainNetwork.layers[i].outputVector.order[0]):
#        value = DQNetwork.MainNetwork.layers[i].outputVector.matrixVals[k][0]
#        newVal = (math.tanh(value) + 1) / 2
#        colourTuple = (255 * newVal, 255 * newVal, 255 * newVal)

#        pygame.draw.rect(window, colourTuple, ((params["WorldSize"] * TW + i * TW * 2), (k * TW * 2), (TW * 2), (TW * 2)))

#worldMap.RenderMap()

#QNetwork.NextStep(worldMap)

#if QNetwork.step > MS:
#    Generate()
#    QNetwork.CreateAgent(worldMap)
#    agent = QNetwork.agent
#    curCycle += 1
#    print(curCycle)

#if curCycle > cycles:
#    QNetwork.SaveQTable()
#    running = False