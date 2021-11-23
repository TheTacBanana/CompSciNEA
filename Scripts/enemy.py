from newAgent import *
from random import randint

class Enemy(Agent): # Enemy inherits from Agent Class
    def __init__(self, location, params): # Constructor for Enemy Class
        self.paramDictionary = params

        self.location = location

        self.alive = True

    def CommitAction(self, agent, worldMap): # Override of Agent Class method
        xDif = agent.location[0] - self.location[0]
        yDif = agent.location[1] - self.location[1]

        if xDif == 0 and yDif == 0: # Checks if on Agent - If so -> Kill Agent
            agent.alive = False
            return

        # Basic Path Finding for enemy
        # Calculates difference between agent and player position, and moves in the greatest direction
        if abs(xDif) > abs(yDif):  # X Dif > Y Dif
            if xDif > 0:
                self.location[0] += 1
            else:
                self.location[0] -= 1
        elif abs(xDif) < abs(yDif): # Y Dif > X Dif
            if yDif > 0:
                self.location[1] += 1
            else:
                self.location[1] -= 1
        else:                       # Move random direction when X Dif = Y Dif
            if randint(0,1):
                if xDif > 0:
                    self.location[0] += 1
                else:
                    self.location[0] -= 1
            else:
                if yDif > 0:
                    self.location[1] += 1
                else:
                    self.location[1] -= 1

        self.alive = self.CheckIfValidStandTile(self.location, worldMap) # Checks if walked into water or not

    @staticmethod
    def SpawnPosition(worldMap, enemyList): # Generate spawn position for the enemy given worldMap and enemyList - Static method
        spawnList = []
        enemyLocList = [enemyList[i].location for i in range(len(enemyList))]

        for y in range(0, worldMap.MAP_SIZE):
            for x in range(0, worldMap.MAP_SIZE):
                if worldMap.tileArray[x][y].tileType == 2: # Checks if tile type is 
                    spawnList.append([x, y])

        shuffle(spawnList)
        
        if spawnList[0] in enemyLocList: # Select spawn if not already selected
            return None
        else:
            return spawnList[0]