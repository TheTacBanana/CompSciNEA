import pickle, random
from agent import Agent

class StateFrame():
    def __init__(self, state, index):
        self.state = state
        self.actionValues = [0 for i in range(5)]
        self.index = index

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

        frame = self.SearchForState(state)

        if frame == None:
            self.AddState(state)

            frame = self.QTable[-1]

            i = self.ChooseRandom(frame.actionValues)
            self.agent.Action(i, worldMap)
        else:
            ep = self.paramDictionary["Epsilon"]
            
            if random.random() < ep:
                i = self.ChooseRandom(frame.actionValues)
            else:
                i = self.ChooseMax(frame.actionValues)

            self.agent.Action(i, worldMap)

        self.step += 1

        tempFrame = StateFrame(self.agent.GetState(worldMap), 0)
        newQSA = self.BellmanEquation(frame, i, tempFrame, self.step)
        #frame.actionValues[i] = newQSA

        #print(self.step, frame.index, i, newQSA)
        self.QTable[frame.index].actionValues[i] = newQSA 

    def BellmanEquation(self, frame, action, newFrame, step): # New Q(s,a) = Q(s,a) + Lr * [R(s,a) + y * maxQ(s, a) - Q(s,a)]
        qsa = frame.actionValues[action]
        lr = self.paramDictionary["LearningRate"]
        y = self.paramDictionary["Gamma"]
        r = self.agent.CalcReward(action, step)
        maxQ = self.MaxQ(newFrame)

        newQSA = qsa + lr * (r + y * maxQ - qsa)
        return newQSA

    def MaxQ(self, state):
        bestAction = None
        bestReward = 0
        for i in range(len(state.actionValues)):
            reward = self.agent.CalcReward(i, self.step)
            if reward > bestReward:
                bestAction = i
                bestReward = reward
        return bestReward

    def SearchForState(self, state):
        for frame in self.QTable:
            if frame.state == state:
                return frame
        return None

    def AddState(self, state):
        self.QTable.append(StateFrame(state, len(self.QTable)))
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