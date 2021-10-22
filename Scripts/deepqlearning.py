import random, pickle
from matrix import Matrix
from copy import copy
import math

class Experience(): 
    def __init__(self, state = None, action = None, reward = None, stateNew = None):
        self.state = state
        self.action = action
        self.reward = reward
        self.stateNew = stateNew

class DoubleNeuralNet():
    def __init__(self, layers, params): # Constructor for a Double Neural Network
        self.paramDictionary = params

        self.MainNetwork = NeuralNet(layers, params)
        self.TargetNetwork = NeuralNet(layers, params)

        self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])
        self.ERBFull = False

        self.epsilon = self.paramDictionary["DQLEpsilon"]

        self.step = 0
        self.cumReward = 0.0
        self.actionsTaken = [0,0,0,0,0]
        self.random = [0,0]

    def TakeStep(self, agent, worldMap):
        self.step += 1

        # Forward Propagation
        netInput = agent.GetStateVector(worldMap) # Retrieve Vector of State info from Agent
        
        self.MainNetwork.ForwardPropagation(netInput) # Forward Prop the Main Network

        output = self.MainNetwork.SoftMax() # Utilise the SoftMax function
                                            # Returns a probability distribution of the outputs of the network

        #print("\n", self.MainNetwork.layers[-1].outputVector)

        # Action Taking and Reward
        #print(output[0])
        if random.random() < self.epsilon: # Epsilon slowly regresses, leaving a greater chance for a random action to be explored
            val = random.random()
            totalled = 0
            for i in range(output[0].order[0]):
                totalled += output[0].matrixVals[i][0]
                #print(val, totalled)
                if totalled >= val:
                    action = i
                    self.random[0] += 1
                    break
            
        else:
            action = output[1]
            self.random[1] += 1

        agent.TakeAction(action, worldMap) # Take Action
        reward = agent.GetRewardWithVector(action, netInput) # Get reward given action

        #print(reward)
        self.cumReward += reward

        # Epsilon Regression
        self.epsilon *= self.paramDictionary["DQLEpisonRegression"] 
        #print(self.epsilon)

        # Assigning values to tempExperience
        tempExp = Experience()
        tempExp.state = netInput 
        tempExp.action = action
        tempExp.reward = reward
        tempExp.stateNew = agent.GetStateVector(worldMap)

        self.actionsTaken[tempExp.action] += 1

        self.ExperienceReplay.PushFront(copy(tempExp))

        # Back Propagation
        Loss = self.LossFunction(output, tempExp, self.MainNetwork.layers, agent)

        for i in range(self.MainNetwork.layers[-1].outputVector.order[0]):
            self.MainNetwork.layers[-1].errSignal.matrixVals[i][0] = Loss

        #self.MainNetwork.BackPropagation()

        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers
            #print("Replaced Weights")

        if not self.ERBFull: # Sample Experience Replay Buffer
            self.ERBFull = self.ExperienceReplay.Full()
        if self.step % self.paramDictionary["ERSampleRate"] == 0 and self.ERBFull: 
            self.SampleExperienceReplay()

        if self.step % 1000 == 0:
            print(self.step, self.cumReward, self.actionsTaken, self.epsilon, self.random)

    def SampleExperienceReplay(self):
        samples = self.ExperienceReplay.Sample(self.paramDictionary["ERSampleSize"])

        for sample in samples:
            pass
            #self.MainNetwork.BackPropagation(sample)

    def LossFunction(self, output, tempExp, prevWeights, agent):
        # L^i(W^i) = (Q(s,a,W) - (r + y*maxQ(s',a';W^i-1)) ** 2

        g = self.paramDictionary["DQLGamma"]

        self.TargetNetwork.ForwardPropagation(tempExp.stateNew)
        targetFeedForward = agent.GetRewardWithVector(self.TargetNetwork.SoftMax()[1], tempExp.stateNew)

        Loss = (agent.GetRewardWithVector(output[1], tempExp.state) - (tempExp.reward + g * targetFeedForward)) ** 2
        return Loss

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

        for i in range(1, len(self.layers) - 1):
            #print(i)
            self.layers[i].ForwardPropagation(self.layers[i-1])

        #print(i+1)
        self.layers[-1].ForwardPropagation(self.layers[-2], finalLayer=True)

    def SoftMax(self): # Implementation of a Soft Max Function
        z = self.layers[-1].outputVector

        sumToK = 0
        maxIndex = 0

        for i in range(z.order[0]):
            sumToK += math.exp(z.matrixVals[i][0])

            if z.matrixVals[i][0] > z.matrixVals[maxIndex][0]:
                maxIndex = i

        outVector = Matrix(z.order)

        for i in range(z.order[0]):
            outVector.matrixVals[i][0] = (math.exp(z.matrixVals[i][0])) / sumToK

        maxVal = outVector.matrixVals[maxIndex][0]

        #print(outVector, maxIndex, maxVal)

        return outVector, maxIndex, maxVal # Returns vector and best index

    def BackPropagation(self, ):
        for i in range(len(self.layers) - 2, -1, -1):
            #print(i)
            self.layers[i].BackPropagation(self.layers[i+1], self.paramDictionary["DQLLearningRate"])

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

        self.errSignal = Matrix((size, 1))
        
        self.outputVector = Matrix((size, 1))

    def ForwardPropagation(self, prevLayer, finalLayer=False):
        weightValueProduct = self.weightMatrix * prevLayer.outputVector

        output = weightValueProduct + self.biasVector

        if not finalLayer:
            for i in range(output.order[0]):
                output.matrixVals[i][0] = math.tanh(output.matrixVals[i][0])  # Tanh Activation 
        else:
            for i in range(output.order[0]):
                output.matrixVals[i][0] = math.tanh(max(0, output.matrixVals[i][0]))  # Tanh and ReLu Activation
        #print("Output", output)
        self.outputVector = output

    def BackPropagation(self, nextLayer, lr):
        transposedWeightMatrix = nextLayer.weightMatrix.Transpose()
        weightUpdates = Matrix(transposedWeightMatrix.order)

        weightErrSigProduct = transposedWeightMatrix * nextLayer.errSignal
        #print(nextLayer.errSignal)

        for i in range(weightUpdates.order[0]): # For every neuron in layer
            z = self.outputVector.matrixVals[i][0]
            zProduct = 1 - (math.tanh(z) ** 2)
            #print(zProduct)

            self.errSignal.matrixVals[i][0] = zProduct * weightErrSigProduct.matrixVals[i][0]

            for k in range(weightUpdates.order[1]):
                weightUpdates.matrixVals[i][k] = -lr * self.errSignal.matrixVals[i][0] * z
        #print(self.errSignal)
        nextLayer.weightMatrix += weightUpdates.Transpose()

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