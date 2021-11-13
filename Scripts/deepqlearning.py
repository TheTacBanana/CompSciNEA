import random, pickle
from matrix import Matrix
from copy import copy
import math

class DoubleNeuralNet(): # Wraps a Main and Target Neural Network together
    def __init__(self, layers, params, load=False, loadNames=["",""]): # Constructor for a Double Neural Network
        self.paramDictionary = params

        if not load:
            self.MainNetwork = NeuralNet(layers, params)
            self.TargetNetwork = NeuralNet(layers, params)
        else:
            self.MainNetwork = NeuralNet.LoadNeuralNet(loadName)
            self.TargetNetwork = NeuralNet.LoadNeuralNet(loadName)

        self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])
        self.ERBFull = False

        self.epsilon = self.paramDictionary["DQLEpsilon"]

        self.step = 0
        self.cumReward = 0.0
        self.actionsTaken = [0,0,0,0,0]
        self.random = [0,0]

    def TakeStep(self, agent, worldMap): # Takes a step forward in time
        self.step += 1
        if self.step == 1000:
            exit()

        # Forward Propagation
        agentSurround = agent.GetTileVector(worldMap)
        postProcessedSurround = agent.TileVectorPostProcess(agentSurround) # Retrieve Vector of State info from Agent
        netInput = postProcessedSurround[1]
        
        self.MainNetwork.ForwardPropagation(netInput) # Forward Prop the Main Network

        output = self.MainNetwork.SoftMax() # Utilise the SoftMax function

        # Action Taking and Reward
        print(output[0])
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
            print(output[1])
            action = output[1]
            self.random[1] += 1

        agent.CommitAction(action, postProcessedSurround[0], worldMap) # Take Action
        reward = agent.GetReward(action, agentSurround) # Get reward given action

        self.cumReward += reward

        # Epsilon Regression
        self.epsilon *= self.paramDictionary["DQLEpisonRegression"] 

        # Assigning values to tempExperience
        tempExp = Experience()
        tempExp.state = agentSurround 
        tempExp.action = action
        tempExp.reward = reward
        tempExp.stateNew = agent.GetTileVector(worldMap)

        self.actionsTaken[tempExp.action] += 1

        self.ExperienceReplay.PushFront(copy(tempExp))

        # Back Propagation
        Loss = self.LossFunction(output, tempExp, self.MainNetwork.layers, agent)

        for i in range(self.MainNetwork.layers[-1].outputVector.order[0]):
            self.MainNetwork.layers[-1].errSignal.matrixVals[i][0] = Loss

        #self.MainNetwork.BackPropagationV1()

        self.MainNetwork.BackPropagationV2()
        #print(self.MainNetwork.layers[-1].weightMatrix.matrixVals[0][0], tempExp.reward)

        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers

        if not self.ERBFull: # Sample Experience Replay Buffer
            self.ERBFull = self.ExperienceReplay.Full()
        if self.step % self.paramDictionary["ERSampleRate"] == 0 and self.ERBFull: 
            self.SampleExperienceReplay()

        if self.step % 1000 == 0:
            print(self.step, self.cumReward, self.actionsTaken, self.epsilon)

    def SampleExperienceReplay(self): # Samples the Experience Replay Buffer, Back Propagating its Findings
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

class NeuralNet(): # Neural Network Implementation
    def __init__(self, layersIn, params): # Constructor for a Single Neural Network
        self.paramDictionary = params

        self.layers = []

        for i in range(len(layersIn)):
            if i == 0:
                self.layers.append(Layer(0, layersIn[0], True))
            else:
                self.layers.append(Layer(layersIn[i - 1], layersIn[i]))

    def ForwardPropagation(self, inputVector): # Iterates through Forward Propagation
        self.layers[0].outputVector = inputVector

        for i in range(1, len(self.layers) - 1):
            self.layers[i].ForwardPropagation(self.layers[i-1])

        self.layers[-1].ForwardPropagation(self.layers[-2], finalLayer=True)

    def SoftMax(self): # Returns a probability distribution of the outputs of the network
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

        return outVector, maxIndex, maxVal # Returns vector and best index

    def BackPropagationV1(self): # Iterates through Back Propagation V1
        for i in range(len(self.layers) - 2, -1, -1):
            self.layers[i].BackPropagationV1(self.layers[i+1], self.paramDictionary["DQLLearningRate"])

    def BackPropagationV2(self): # Iterates through Back Propagation V2
        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i].BackPropagationV2(self.layers[i-1], self.paramDictionary["DQLLearningRate"])

    # Using Pickle to Save/Load
    @staticmethod
    def LoadNeuralNet(file): # Returns stored Neural Network data
        with open("DQLearningData\\" + file + ".dqn", "rb") as f:
            temp = pickle.load(f)
        return temp

    def SaveNeuralNet(self, file): # Saves Neural Network Data
        with open("DQLearningData\\" + file + ".dqn", "wb") as f:
            pickle.dump(self, f)

class Layer(): # Layer for a Neural Network
    def __init__(self, prevSize, size, inputLayer=False):
        if inputLayer == False:
            self.weightMatrix = Matrix((size, prevSize), random=True)

            self.biasVector = Matrix((size, 1), random=False)

        self.errSignal = Matrix((size, 1))
        
        self.sVector = Matrix((size, 1))
        self.outputVector = Matrix((size, 1))

    def ForwardPropagation(self, prevLayer, finalLayer=False): # Forward Propagates the Neural Network
        weightValueProduct = self.weightMatrix * prevLayer.outputVector

        self.sVector = weightValueProduct + self.biasVector

        if not finalLayer:
            for i in range(self.sVector.order[0]):
                self.outputVector.matrixVals[i][0] = Layer.Sigmoid(self.sVector.matrixVals[i][0])  # Sigmoid Activation
        else:
            for i in range(self.sVector.order[0]):
                self.outputVector.matrixVals[i][0] = max(0, Layer.Sigmoid(self.sVector.matrixVals[i][0]))  # ReLu Activation

    @staticmethod
    def Sigmoid(x): # Mathematical Function to get "squish" values between 0 and 1
        if x > 10:
            return 1
        elif x < -10:
            return 0
        else:
            return 1 / (1 + math.exp(-x))

    def BackPropagationV1(self, nextLayer, lr): # 1st Revision of Back Prop -> Does not work
        transposedWeightMatrix = nextLayer.weightMatrix.Transpose()
        weightUpdates = Matrix(transposedWeightMatrix.order)

        weightErrSigProduct = transposedWeightMatrix * nextLayer.errSignal

        for i in range(weightUpdates.order[0]): # For every neuron in layer
            s = self.sVector.matrixVals[i][0]
            z = self.outputVector.matrixVals[i][0]
            zDerivative = 1 - (math.tanh(s) ** 2)

            self.errSignal.matrixVals[i][0] = zDerivative * weightErrSigProduct.matrixVals[i][0]

            for k in range(weightUpdates.order[1]):
                weightUpdates.matrixVals[i][k] = -lr * self.errSignal.matrixVals[i][0] * z
        nextLayer.weightMatrix += weightUpdates.Transpose()

    def BackPropagationV2(self, prevLayer, lr): # 2nd Revision of Back Prop -> Might work :)
        # Calculating Next Error Signal
        halfErrSignal = (self.weightMatrix.Transpose() * self.errSignal)

        zDerivative = prevLayer.sVector
        for i in range(zDerivative.order[0]):
            z = zDerivative.matrixVals[i][0]
            zDerivative.matrixVals[i][0] = Layer.Sigmoid(z) * (1 - Layer.Sigmoid(z))

        errSignal = halfErrSignal * zDerivative # Hadamard Product
        prevLayer.errSignal = errSignal

        # Calculating Weight updates
        updatedWeightVectors = []
        for delta in range(self.errSignal.order[0]):
            errSignal = self.errSignal.matrixVals[delta][0]

            selectedColumn = self.weightMatrix.Transpose().SelectColumn(delta)
            updatedWeightVectors.append(selectedColumn * errSignal * (-lr))

        updatedWeights = Matrix.CombineVectorsHor(updatedWeightVectors)
        print(updatedWeights.order, self.weightMatrix.order)
        self.weightMatrix += updatedWeights.Transpose()

class Experience(): # Used in Experience Replay
    def __init__(self, state = None, action = None, reward = None, stateNew = None): # Constructor for an Experience Replay Experience
        self.state = state
        self.action = action
        self.reward = reward
        self.stateNew = stateNew

class Deque(): # Partial Double Ended Queue Implementation
    def __init__(self, length):
        self.length = length

        self.queue = [None for i in range(self.length)]

        self.frontP = -1
        self.backP = -1

    def PushFront(self, item): # Pushes item to front of Queue
        self.frontP = (self.frontP + 1) % self.length

        if self.queue[self.frontP] != None:
            self.backP = (self.frontP + 1) % self.length

        self.queue[self.frontP] = item

    def Full(self): # Checks if Queue is full
        if self.queue[self.length - 1] != None:
            return True
        return False

    def First(self): # Returns Front Item from Queue
        return self.queue[self.frontP]

    def Last(self): # Returns Final Item from Queue
        return self.queue[self.backP]

    def Sample(self, n): # Samples N number of samples from the deque
        temp = self.queue
        return random.sample(temp, n)