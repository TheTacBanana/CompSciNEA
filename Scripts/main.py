from worldClass import *
from qlearning import *
import pygame

# Constant variables
worldSeed = 0
params = WorldMap.LoadParameters("Default")
worldMap = WorldMap(worldSeed, params)

headless = params["Headless"]
if not headless:
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

QNetwork = QLearning(params)
QNetwork.CreateAgent(worldMap)
agent = QNetwork.agent
TW = params["TileWidth"]
MS = params["QLearningMaxSteps"]

curCycle = 0
cycles = 10

QNetwork.LoadQTable()

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

        #worldMap.RenderMap()
        
        QNetwork.NextStep(worldMap)
        worldMap.DrawMap(window)

        if QNetwork.step > MS:
            Generate()
            QNetwork.CreateAgent(worldMap)
            agent = QNetwork.agent
            curCycle += 1
            print(curCycle)

        if curCycle > cycles:
            QNetwork.SaveQTable()
            running = False
        
        pygame.draw.rect(window, (233, 182, 14), ((agent.location[0] * TW), (agent.location[1] * TW), TW, TW))

        pygame.display.update()
    else:
        pass