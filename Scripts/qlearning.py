import pickle

class StateFrame():
    def __init__(self, state):
        self.state = state

        self.actionValues = [0 for i in range(5)]

class QLearning():
    def __init__(self, params):
        self.paramDictionary = params

        self.QTable = []

    def NextState(self,worldMap):
        pass

    def SearchForState(self, state):
        for frame in self.QTable:
            if frame.state == state:
                return frame.actionValues

    def AddState(self, state):
        self.QTable.append(StateFrame(state))
    
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
            pickle.dumps(QTable, f)

    def LoadQTable(self, filename):
        with open(input("Input File Name: "), "rb") as f:
            x = pickle.load(f)

        self.QTable = x