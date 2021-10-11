import random, pickle
from matrix import Matrix
from collections import namedtuple

StateTuple = namedtuple("StateTuple", ["State", "Action", "Reward", "StateNew"])


class DoubleNeuralNet():
    def __init__(self, layers, params):
        self.paramDictionary = params

        self.MainNetwork = NeuralNet(layers, params)
        self.TargetNetwork = NeuralNet(layers, params)

        self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])
        self.ERBFull = False

        self.step = 0

    def TakeStep(self, agent, worldMap):
        self.step += 1

        netInput = agent.StateVector(worldMap)

        # Forward Propagation
        self.MainNetwork.ForwardPropagation(netInput)
        self.TargetNetwork.ForwardPropagation(netInput)

        #self.MainNetwork.SoftMax()

        #Back Propagation
        #cost = self.MainNetwork.BellmanEquation()

        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers

        if not self.ERBFull:
            self.ERBFull = self.ExperienceReplay.Full()

        if self.step % self.paramDictionary["ERSampleRate"] == 0 and self.ERBFull: # Sample Experience Replay Buffer
            self.SampleExperienceReplay()

    def SampleExperienceReplay(self):
        samples = self.ExperienceReplay.Sample(self.paramDictionary["ERSampleSize"]) # Samples Experience Replay Buffer

        for sample in samples:
            self.MainNetwork.BackPropagation(sample)

class NeuralNet():
    def __init__(self, layers, params):
        self.paramDictionary = params

        self.layers = []

        for i in range(len(layers)):
            if i == 0:
                self.layers.append(Layer(0, layers[0]))
            else:
                self.layers.append(Layer(layers[i - 1], layers[i]))

    def ForwardPropagation(self, inputVector):
        self.layers[0].outputVector = inputVector

        for i in range(1, len(self.layers)):
            self.layers[i].ForwardPropagation(self.layers[i-1])

    def SoftMax(self): # Implementation of a Soft Max Function
        z = self.layers[-1].outputVector
        sumToK = 0
        maxIndex = 0

        for i in range(z.order[0]):
            sumToK += z.matrixVals[i][0]

            if z.matrixVals[i][0] > z.matrixVals[maxIndex][0]:
                maxIndex = i

        outVector = Matrix(z.order)

        for i in range(z.order[0]):
            outVector.matrixVals[i][0] = z.matrixVals[i][0] / sumToK

        return outVector, maxIndex

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
            self.weightMatrix = Matrix((prevSize, size), random=True)

            self.biasVector = Matrix((size, 1))
        
        self.outputVector = Matrix((1, size))

    def ForwardPropagation(self, prevLayer):
        weightValueProduct = self.weightMatrix * prevLayer.output

        output = weightValueProduct + self.biasVector

        for i in range(output.order[0]):
            output[i][0] = max(0, output[i][0]) # ReLU Activation Function

        self.output = output

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