import pickle, random
from agent import Agent

class StateFrame():
    def __init__(self, state):
        self.state = state

        self.actionValues = [0 for i in range(5)]

class QLearning():
    def __init__(self, params):
        self.paramDictionary = params

        self.QTable = []

        self.step = 0
        
    def CreateAgent(self, worldMap):
        spawnPos = Agent.SpawnPosition(worldMap)
        self.agent = Agent(spawnPos, self.paramDictionary)

    def NextStep(self, worldMap):
        state = self.agent.GetState(worldMap)

        actionVals = self.SearchForState(state)

        if actionVals == None:
            self.AddState(state)

            actionVals = self.SearchForState(state)

            i = self.ChooseRandom(actionVals)
            self.agent.Action(i, worldMap)
        else:
            ep = self.paramDictionary["Epsilon"]
            
            if random.random() < ep:
                i = self.ChooseRandom(actionVals)
            else:
                i = self.ChooseMax(actionVals)

            self.agent.Action(i, worldMap)

        self.step += 1

    def SearchForState(self, state):
        for frame in self.QTable:
            if frame.state == state:
                return frame.actionValues
        return None

    def AddState(self, state):
        self.QTable.append(StateFrame(state))
        #print("Added State")
    
    def ChooseRandom(self, values):
        return random.randint(0, len(values) - 1)

    def ChooseMax(self, values):
        maxIndex = 0
        for i in range(len(values)):
            if values[i] > values[maxIndex]:
                maxIndex = i
        return maxIndex

    def SaveQTable(self):
        with open(input("Input File Name: "), "wb") as f:
            pickle.dumps(self.QTable, f)

    def LoadQTable(self, filename):
        with open(input("Input File Name: "), "rb") as f:
            x = pickle.load(f)

        self.QTable = x