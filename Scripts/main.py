import pygame
from worldClass import *
import mathlib

# Constant variables
worldSeed = 0
worldMap = WorldMap(worldSeed, WorldMap.LoadParameters("Default"))

worldResolution = worldMap.MAP_SIZE * worldMap.TILE_WIDTH
window = pygame.display.set_mode((worldResolution, worldResolution))

# Generates and renders the map to a single surface for optimisation
worldMap.GenerateMap()
worldMap.RenderMap()

# Constant loop running
running = True
while running == True:
    worldMap.DrawMap(window)

    pygame.display.update()