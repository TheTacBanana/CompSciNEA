import pygame
from simulation import *
import time
import datalogger

params = Simulation.LoadParameters("Default")
stepDelay = params["StepDelay"]
Simulation.CheckParameters(params, "Range")

gameSim = Simulation(1, params)
gameSim.InitiateSimulation()

worldResolution = params["WorldSize"] * params["TileWidth"]
if params["Debug"]: debugOffset = (len(params["DeepQLearningLayers"]) * params["TileWidth"] * params["DebugScale"])
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
            if event.key == pygame.K_F2:
                gameSim.agent.alive = False

    gameSim.TimeStep()
    time.sleep(stepDelay)

    gameSim.RenderToCanvas(window, params["Debug"])  

    pygame.display.update()

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