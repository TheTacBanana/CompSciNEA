import pygame
from worldClass import *
import mathlib

WORLD_SIZE = 50
TILE_WIDTH = 10
WORLD_SEED = 0
worldMap = WorldMap(WORLD_SIZE, TILE_WIDTH, WORLD_SEED)

window = pygame.display.set_mode((WORLD_SIZE * TILE_WIDTH, WORLD_SIZE * TILE_WIDTH))


worldMap.GenerateMap()
worldMap.RenderMap()
worldMap.DrawMap(window)
#worldMap.ConsoleOut()

matrix1 = mathlib.Matrix([[1, 2],[3, 4]])
print(matrix1.Val())

running = True
while running == True:
    worldMap.DrawMap(window)

    pygame.display.update()