import random, pickle
from matrix import Matrix

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

    # Using Pickle to Save/Load
    @classmethod
    def LoadNeuralNet(file): # Returns stores Neural Network data
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

class PriorityDeque(): # Double Ended Priority Queue
    pass

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

    def First(self):
        return self.queue[self.frontP]

    def Last(self):
        return self.queue[self.backP]

    def Sample(self, n):
        temp = self.queue
        return random.sample(temp, n)

dq = Deque(10)

for i in range(100):
    dq.PushFront(i)

print(dq.Sample(2))

        