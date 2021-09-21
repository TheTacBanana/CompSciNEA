from worldClass import *
from agent import *
import mathlib, threading

# Constant variables
worldSeed = 0
params = WorldMap.LoadParameters("Default")
worldMap = WorldMap(worldSeed, params)

headless = params["Headless"]
if not headless:
    #import pygame
    print(pygame)
    worldResolution = worldMap.MAP_SIZE * worldMap.TILE_WIDTH
    window = pygame.display.set_mode((worldResolution, worldResolution))

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

agent = Agent(Agent.SpawnPosition(worldMap), params)
print(agent.GetState(worldMap))


#print(worldMap.ConsoleOut())
#tick = 0

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

        worldMap.RenderMap()
        worldMap.DrawMap(window)
        pygame.display.update()
    else:
        pass