from newAgent import *
from random import randint

class Enemy(Agent):
    def __init__(self, location, params):
        self.paramDictionary = params

        self.location = location

        self.alive = True

    def CommitAction(self, agent, worldMap): # Rewrite Agent Action Method
        xDif = agent.location[0] - self.location[0]
        yDif = agent.location[1] - self.location[1]

        if xDif == 0 and yDif == 0:
            agent.alive = False
            return

        if abs(xDif) > abs(yDif):
            if xDif > 0:
                self.location[0] += 1
            else:
                self.location[0] -= 1
        elif abs(xDif) < abs(yDif):
            if yDif > 0:
                self.location[1] += 1
            else:
                self.location[1] -= 1
        else:
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

        self.alive = self.CheckIfValidStandTile(self.location, worldMap)

    @staticmethod
    def SpawnPosition(worldMap, enemyList):
        spawnList = []
        enemyLocList = [enemyList[i].location for i in range(len(enemyList))]

        for y in range(0, worldMap.MAP_SIZE):
            for x in range(0, worldMap.MAP_SIZE):
                if worldMap.tileArray[x][y].tileType == 2:
                    spawnList.append([x, y])

        shuffle(spawnList)
        
        if spawnList[0] in enemyLocList:
            return None
        else:
            return spawnList[0]