import pygame
from worldClass import *
import mathlib

# Constant variables
WORLD_SIZE = 100
TILE_WIDTH = 10
TILE_BORDER = 1
WORLD_SEED = 0

worldMap = WorldMap(WORLD_SIZE, TILE_WIDTH, TILE_BORDER, WORLD_SEED)

worldResolution = WORLD_SIZE * TILE_WIDTH
window = pygame.display.set_mode((worldResolution, worldResolution))

# Generates and renders the map to a single surface for optimisation
worldMap.GenerateMap()
worldMap.RenderMap()

# Constant loop running
running = True
while running == True:
    worldMap.DrawMap(window)

    pygame.display.update()