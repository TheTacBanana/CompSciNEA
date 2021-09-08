from worldClass import *
import mathlib, threading

# Constant variables
worldSeed = 0
print(worldSeed)
worldMap = WorldMap(worldSeed, WorldMap.LoadParameters("Default"))

headless = worldMap.paramDictionary["Headless"]
if not headless:
    import pygame
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
#tick = 0

# Constant loop running
running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(client.close())
            running = False

        if event.type == pygame.KEYDOWN: # Key Down
            if event.key == pygame.K_F1:
                Generate()
    
    if not headless:
        worldMap.RenderMap()
        worldMap.DrawMap(window)
        pygame.display.update()