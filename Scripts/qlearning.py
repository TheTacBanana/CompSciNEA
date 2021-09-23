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
        self.cumReward = 0
        
    def CreateAgent(self, worldMap):
        spawnPos = Agent.SpawnPosition(worldMap)
        self.agent = Agent(spawnPos, self.paramDictionary)
        self.step = 0
        self.cumReward = 0

    def NextStep(self, worldMap):
        state = self.agent.GetState(worldMap)

        frame = self.SearchForState(state)
        reward = 0

        if frame == None:
            self.AddState(state)

            frame = self.QTable[-1]

            i = self.ChooseRandom(frame.actionValues)
            reward = self.agent.Action(i, worldMap)
        else:
            ep = self.paramDictionary["Epsilon"]
            
            if random.random() < ep:
                i = self.ChooseRandom(frame.actionValues)
            else:
                i = self.ChooseMax(frame.actionValues)

            reward = self.agent.Action(i, worldMap)

        self.step += 1
        self.cumReward += reward
        #print(self.cumReward)
        print(self.step)

        tempFrame = StateFrame(self.agent.GetState(worldMap), 0)
        newQSA = self.BellmanEquation(frame, i, tempFrame, reward, self.step, worldMap)
        #frame.actionValues[i] = newQSA

        #print(self.step, frame.index, i, newQSA)
        self.QTable[frame.index].actionValues[i] = newQSA 

    def BellmanEquation(self, frame, action, newFrame, reward, step, worldMap): # New Q(s,a) = Q(s,a) + Lr * [R(s,a) + y * maxQ(s, a) - Q(s,a)]
        qsa = frame.actionValues[action]
        lr = self.paramDictionary["LearningRate"]
        y = self.paramDictionary["Gamma"]
        r = reward
        maxQ = self.MaxQ(newFrame, worldMap)

        newQSA = qsa + lr * (r + y * maxQ - qsa)
        return newQSA

    def MaxQ(self, state, worldMap):
        bestAction = None
        bestReward = 0
        for i in range(len(state.actionValues)):
            reward = self.agent.Action(i, worldMap, True)
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
        with open("QLearningData\\{}.qd".format(input("Input File Name: ")), "wb") as f:
            pickle.dump(self.QTable, f)

    def LoadQTable(self):
        with open("QLearningData\\{}.qd".format(input("Input File Name: ")), "rb") as f:
            x = pickle.load(f)

        self.QTable = x