import pygame
from simulation import *
import time

params = Simulation.LoadParameters("Default") # Loads parameters
Simulation.CheckParameters(params, "Range") # Checks parameters

gameSim = Simulation(1, params) # Create and initiate simulation
gameSim.InitiateSimulation()

# Creates pygame window - includes side debug offset if needed
worldResolution = params["WorldSize"] * params["TileWidth"] 
if params["Debug"]: 
    debugOffset = (len(params["DeepQLearningLayers"]) * params["TileWidth"] * params["DebugScale"])
else: 
    debugOffset = 0
window = pygame.display.set_mode((worldResolution + debugOffset, worldResolution))

stepDelay = params["StepDelay"] # Time step Delay

# Constant loop running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If window exit than close end program
            running = False

        if event.type == pygame.KEYDOWN: # Key Down
            if event.key == pygame.K_F1: # Force Create new world
                gameSim.CreateWorld()
            if event.key == pygame.K_F2: # Force Kill agent
                gameSim.agent.alive = False

    gameSim.TimeStep() # Perform a timestep
    time.sleep(stepDelay) # Sleep if needed

    gameSim.RenderToCanvas(window) # Draw to canvas

    pygame.display.update() # Update pygame window to display content