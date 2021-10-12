import random, pickle
from matrix import Matrix
from collections import namedtuple
from copy import copy

StateTuple = namedtuple("StateTuple", ["State", "Action", "Reward", "StateNew"])

class Experience():
    def __init__(self, state = None, action = None, reward = None, stateNew = None):
        self.state = state
        self.action = action
        self.reward = reward
        self.stateNew = stateNew

class DoubleNeuralNet():
    def __init__(self, layers, params):
        self.paramDictionary = params

        self.MainNetwork = NeuralNet(layers, params)
        self.TargetNetwork = NeuralNet(layers, params)

        self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])
        self.ERBFull = False

        self.epsilon = self.paramDictionary["DQLEpsilon"]

        self.step = 0

    def TakeStep(self, agent, worldMap):
        self.step += 1
        tempExp = Experience()

        # Forward Propagation
        netInput = agent.GetStateVector(worldMap) # Retrieve Vector of State info from Agent
        
        self.MainNetwork.ForwardPropagation(netInput) # Forward Prop the Main Network
        print(self.MainNetwork.layers[4].outputVector)

        output = self.MainNetwork.SoftMax() # Utilise the SoftMax function
                                            # Returns a probability distribution of the outputs of the network

        # Epsilon Regression - Taking actions
        if random.random() > self.epsilon:
            val = random.random
            totalled = 0
            for i in range(output.order()[0]):
                totalled += output[0].matrixVals[i][0]
                if totalled <= val:
                    action = i
        else:
            action = output[1]
        self.epsilon *= self.paramDictionary["DQLEpisonRegression"]

        reward = agent.ActionNew(action, worldMap) # Take Action
        #reward = agent.RewardNew(action) # Get reward given action

        # Assigning values to tempExperience
        tempExp.state = netInput 
        tempExp.action = output[1]
        tempExp.reward = reward
        tempExp.stateNew = agent.StateVector()

        self.ExperienceReplay.PushFront(copy(tempExp))

        #Cost Function
        # Cost = [QSA(Main) - (Reward(SA) + Gamma * SoftMax(QS'A(Target)))]^2
        g = self.paramDictionary["DQLGamma"]
        self.TargetNetwork.ForwardPropagation(tempExp.stateNew)
        TQSA = self.TargetNetwork.SoftMax()

        cost = (output[0] - (reward + g * TQSA[0])) ** 2
        #print(cost)

        # Back Propagation


        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers

        if not self.ERBFull: # Sample Experience Replay Buffer
            self.ERBFull = self.ExperienceReplay.Full()
        if self.step % self.paramDictionary["ERSampleRate"] == 0 and self.ERBFull: 
            self.SampleExperienceReplay()

    def SampleExperienceReplay(self):
        samples = self.ExperienceReplay.Sample(self.paramDictionary["ERSampleSize"])

        for sample in samples:
            self.MainNetwork.BackPropagation(sample)

class NeuralNet():
    def __init__(self, layers, params):
        self.paramDictionary = params

        self.layers = []

        for i in range(len(layers)):
            if i == 0:
                self.layers.append(Layer(0, layers[0], True))
            else:
                self.layers.append(Layer(layers[i - 1], layers[i]))

    def ForwardPropagation(self, inputVector):
        self.layers[0].outputVector = inputVector

        for i in range(1, len(self.layers)):
            self.layers[i].ForwardPropagation(self.layers[i-1])

    def SoftMax(self): # Implementation of a Soft Max Function
        z = self.layers[4].outputVector
        print(z)
        sumToK = 0
        maxIndex = 0

        for i in range(z.order[0]):
            sumToK += z.matrixVals[i][0]

            if z.matrixVals[i][0] > z.matrixVals[maxIndex][0]:
                maxIndex = i

        outVector = Matrix(z.order)

        for i in range(z.order[0]):
            outVector.matrixVals[i][0] = z.matrixVals[i][0] / sumToK

        return outVector, maxIndex # Returns vector and best index

    def Cost(self):
        pass

    # Using Pickle to Save/Load
    @classmethod
    def LoadNeuralNet(file): # Returns stored Neural Network data
        with open(file, "rb") as f:
            temp = pickle.load(f)
        return temp

    def SaveNeuralNet(self, file): # Saves Neural Network Data
        with open(file, "wb") as f:
            pickle.dump(self, f)

class Layer():
    def __init__(self, prevSize, size, inputLayer=False):
        if inputLayer == False:
            self.weightMatrix = Matrix((size, prevSize), random=True)

            self.biasVector = Matrix((size, 1), random=True)
        
        self.outputVector = Matrix((size, 1))

    def ForwardPropagation(self, prevLayer):
        weightValueProduct = self.weightMatrix * prevLayer.outputVector

        self.outputVector = weightValueProduct + self.biasVector
        print(self.outputVector)

        #for i in range(output.order[0]):
        #    output.matrixVals[i][0] = max(0, output.matrixVals[i][0]) # ReLU Activation Function
        #print(output.order)

        #self.output = output

class Deque(): # Double Ended Queue 
    def __init__(self, length):
        self.length = length

        self.queue = [None for i in range(self.length)]

        self.frontP = -1
        self.backP = -1

    def PushFront(self, item):
        self.frontP = (self.frontP + 1) % self.length

        if self.queue[self.frontP] != None:
            self.backP = (self.frontP + 1) % self.length

        self.queue[self.frontP] = item

    def Full(self):
        if self.queue[self.length - 1] != None:
            return True
        return False

    def First(self):
        return self.queue[self.frontP]

    def Last(self):
        return self.queue[self.backP]

    def Sample(self, n): # Samples N number of samples from the deque
        temp = self.queue
        return random.sample(temp, n) 