import pygame
from worldClass import *
import mathlib

# Constant variables
worldSeed = random.randint(10000, 99999)
print(worldSeed)
worldMap = WorldMap(worldSeed, WorldMap.LoadParameters("Default"))

worldResolution = worldMap.MAP_SIZE * worldMap.TILE_WIDTH
window = pygame.display.set_mode((worldResolution, worldResolution))

# Generates and renders the map to a single surface for optimisation
def Generate():
    global worldMap
    #worldMap.MAP_SEED = random.randint(100000, 999999)
    worldMap.GenerateMap()
    worldMap.RenderMap()

Generate()
tick = 0

# Constant loop running
running = True
while running == True:
    worldMap.DrawMap(window)

    Generate()
    pygame.image.save(window,"GifFolder\\img{}.png".format(tick))
    tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(client.close())
            running = False

        if event.type == pygame.KEYDOWN: # Key Down
            if event.key == pygame.K_F1:
                Generate()
    
    pygame.display.update()