import pygame
from worldClass import *

WORLD_SIZE = 10
TILE_WIDTH = 10
WORLD_SEED = 0
worldMap = WorldMap(WORLD_SIZE, TILE_WIDTH, WORLD_SEED)

window = pygame.display.set_mode((WORLD_SIZE * TILE_WIDTH, WORLD_SIZE * TILE_WIDTH))

worldMap.GenerateMap()
worldMap.RenderMap()

running = True
while running == True:
    worldMap.DrawMap(window)

