from audioop import bias
import random, pickle, math
from typing import final
from matrix import Matrix
import activations
from copy import copy
from datalogger import *
import time

class DoubleNeuralNet(): # Wraps a Main and Target Neural Network together
    def __init__(self, layers, params, load=False, loadName="DQNetwork"): # Constructor for a Double Neural Network
        self.paramDictionary = params

        if not load: # Create brand new values
            self.MainNetwork = NeuralNet(layers, params)
            self.TargetNetwork = NeuralNet(layers, params)

            self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])

            self.epsilon = self.paramDictionary["DQLEpsilon"]

            self.step = 0
            self.cumReward = 0.0
            
            self.layerActivation = activations.Sigmoid()
            self.finalLayerActivation = activations.SoftMax()
        else:
            self.LoadState(loadName) # Load values from saved data

        self.fileName = loadName
        
        self.activations = (self.layerActivation, self.finalLayerActivation) # Tuple of activations

        self.batchReward = 0
        self.maxBatchReward = 0
        self.batchLoss = 0
        self.dataPoints = []

                                                        # BatchReward, MaxBatchReward, PercentageDifference, Step
        self.actionTracker = DataLogger("ActionTracker", [[float, int], [float, int], [float, int], int], False)

        self.startTime = time.time()

    def TakeStep(self, agent, worldMap, enemyList): # Takes a step forward in time
        self.step += 1

        # Forward Propagation
        agentSurround = agent.GetTileVector(worldMap, enemyList)
        postProcessedSurround = agent.TileVectorPostProcess(agentSurround) # Retrieve Vector of State info from Agent
        netInput = postProcessedSurround[1]
        
        self.MainNetwork.ForwardPropagation(netInput, self.activations) # Forward Prop the Main Network

        output = self.MainNetwork.layers[-1].activations
        #print(output)
        outputMax = output.MaxInVector()

        # Action Taking and Reward
        if random.random() > self.epsilon:
            softmaxxed = self.finalLayerActivation.Activation(copy(output))
            action = random.randint(0, self.paramDictionary["DeepQLearningLayers"][-1] - 1)
            val = random.random()
            totalled = 0
            for i in range(softmaxxed.order[0]):
                totalled += softmaxxed.matrixVals[i][0]
                if totalled >= val:
                    action = i
                    break
        else:
            action = random.randint(0, self.paramDictionary["DeepQLearningLayers"][-1] - 1)

        rewardVector = agent.GetRewardVector(agentSurround, self.paramDictionary["DeepQLearningLayers"][-1])
        reward = rewardVector.matrixVals[action][0] # Get reward given action
        self.cumReward += reward
        self.batchReward += reward
        self.maxBatchReward += rewardVector.MaxInVector()[0]

        agent.CommitAction(action, agentSurround, worldMap, enemyList) # Take Action
        # Epsilon Regression
        self.epsilon *= self.paramDictionary["DQLEpisonRegression"] 

        # Assigning values to tempExperience
        tempExp = Experience()
        tempExp.state = agentSurround 
        tempExp.action = action
        tempExp.reward = rewardVector
        tempExp.stateNew = agent.GetTileVector(worldMap, enemyList)

        self.ExperienceReplay.PushFront(copy(tempExp))

        # Back Propagation
        expectedValues = self.ExpectedValue(output, tempExp, agent) # Calculating Loss

        Cost = self.HalfSquareDiff(output, expectedValues)

        self.batchLoss += Cost.Sum()

        self.MainNetwork.layers[-1].errSignal = Cost * self.layerActivation.Derivative(copy(self.MainNetwork.layers[-1].preactivations))

        self.MainNetwork.BackPropagationV2(self.activations) # Back Propagating the loss

        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers

        # Sample Experience Replay Buffer
        if (self.paramDictionary["EREnabled"] and self.step % self.paramDictionary["ERSampleRate"] == 0 and self.ExperienceReplay.Full()): 
            self.SampleExperienceReplay(agent)

        # Actions to run after every Batch
        if self.step % self.paramDictionary["DQLEpoch"] == 0: 
            print(self.step, self.cumReward, self.epsilon, time.time() - self.startTime)

            self.MainNetwork.UpdateWeightsAndBiases(self.paramDictionary["DQLEpoch"]) # Update weights and biases

            if self.paramDictionary["SaveWeights"]: # Saves weights if specified
                self.SaveState(self.fileName)

            #Log Action
            self.actionTracker.LogDataPoint([self.batchReward, self.maxBatchReward, self.batchLoss, self.step])
            #self.actionTracker.LogDataPointBatch(self.dataPoints)

            self.dataPoints = []
            self.actionTracker.SaveDataPoints()

            self.batchReward = 0
            self.maxBatchReward = 0
            self.batchLoss = 0

    def SampleExperienceReplay(self, agent): # Samples the Experience Replay Buffer, Back Propagating its Findings
        samples = self.ExperienceReplay.Sample(self.paramDictionary["ERSampleSize"])

        for sample in samples:
            postProcessedSurround = agent.TileVectorPostProcess(sample.state) # Post process the Tile Vector
            netInput = postProcessedSurround[1]

            self.MainNetwork.ForwardPropagation(netInput, self.activations) # Forward Prop the Main Network

            output = self.MainNetwork.layers[-1].activations

            expectedValues = self.ExpectedValue(output, sample, agent) # Calculating Loss

            Cost = self.HalfSquareDiff(output, expectedValues)

            self.MainNetwork.layers[-1].errSignal = Cost * self.layerActivation.Derivative(copy(self.MainNetwork.layers[-1].preactivations))

            self.MainNetwork.BackPropagationV2(self.activations) # Back Propagating the loss

    def HalfSquareDiff(self, networkOutput, expected):
        return ((expected - networkOutput) ** 2) * 0.5

    def ExpectedValue(self, output, tempExp, agent):
        # L^i(W^i) = ((r + y*maxQ(s',a';W^i-1) - Q(s,a,W)) ** 2
        # Loss = ((Reward[] + Gamma * MaxQ(s', a'; TNet)) - Q(s, a)[]) ^ 2

        Reward = tempExp.reward
        Gamma = self.paramDictionary["DQLGamma"]

        #self.TargetNetwork.ForwardPropagation(agent.TileVectorPostProcess(tempExp.state)[1], self.activations) # Apply input to Target Network
        
        #targetNetAction = self.TargetNetwork.layers[-1].activations.MaxInVector()[1]


        tempRewardVec = agent.GetRewardVector(tempExp.stateNew, self.paramDictionary["DeepQLearningLayers"][-1]) # Gets reward vector from the new state
        maxQTNet = agent.MaxQ(tempRewardVec) # Max of Target network

        LossVec = ((Reward + (Gamma * maxQTNet)) - output) ** 2 # Bellman Equation
        return LossVec

    def SaveState(self, file):
        state = [self.MainNetwork, self.TargetNetwork, self.ExperienceReplay, self.step, 
                    self.epsilon, self.cumReward, self.layerActivation, self.finalLayerActivation]
        with open("DQLearningData\\" + file + ".dqn", "wb") as f:
            pickle.dump(state, f)

    def LoadState(self, file): # Returns stored Neural Network data
        with open("DQLearningData\\" + file + ".dqn", "rb") as f:
            state = pickle.load(f)

            self.MainNetwork = state[0]
            self.TargetNetwork = state[1]
            self.ExperienceReplay = state[2]
            self.step = state[3]
            self.epsilon = state[4]
            self.cumReward = state[5]
            self.layerActivation = state[6]
            self.finalLayerActivation = state[7]

class NeuralNet(): # Neural Network Implementation
    def __init__(self, layersIn, params): # Constructor for a Single Neural Network
        self.paramDictionary = params

        newLayersIn = copy(layersIn)

        newLayersIn.append(1)

        self.layers = []

        for i in range(len(newLayersIn) - 1):
            print(newLayersIn[i])
            self.layers.append(Layer(newLayersIn[i], newLayersIn[i + 1]))

    def ForwardPropagation(self, inputVector, activations): # Iterates through Forward Propagation
        self.layers[0].activations = inputVector

        for i in range(0, len(self.layers) - 1):
            self.layers[i].ForwardPropagation(self.layers[i+1], activations)

        #self.layers[-1].ForwardPropagation(self.layers[-2], activations, finalLayer=True)

    def BackPropagationV2(self, activations): # Iterates through Back Propagation V2
        self.layers[-2].BackPropagationV2(self.layers[-1], self.paramDictionary["DQLLearningRate"], activations)

        for i in range(len(self.layers) - 3, 0, -1):
            self.layers[i].BackPropagationV2(self.layers[i+1], self.paramDictionary["DQLLearningRate"], activations)

    def UpdateWeightsAndBiases(self, epochCount): # Update Weights and biases
        for i in range(1, len(self.layers)):
            self.layers[i].UpdateWeightsAndBiases(epochCount)

class Layer(): # Layer for a Neural Network
    def __init__(self, size, nextSize, inputLayer=False): # Constructor for a Layer Object
        if inputLayer == False: # Additional objects if not the input layer
            pass

        self.weightMatrix = Matrix((nextSize, size), random=True)
        self.biasVector = Matrix((nextSize, 1), random=False)

        self.weightUpdates = Matrix((nextSize, size))
        self.biasUpdates = Matrix((nextSize, 1))

        self.errSignal = Matrix((nextSize, 1))
        self.preactivations = Matrix((size, 1))
        self.activations = Matrix((size, 1))

    def ForwardPropagation(self, nextLayer, activations): # Forward Propagates the Neural Network
        self.preactivations = self.weightMatrix * self.activations + self.biasVector

        nextLayer.activations = activations[0].Activation(copy(self.preactivations))

    def BackPropagationV2(self, prevLayer, lr, layerActivations): # 2nd Revision of Back Propagation
        deltaWeightProduct = (prevLayer.weightMatrix.Transpose() * prevLayer.errSignal)
        self.errSignal = deltaWeightProduct * layerActivations[0].Derivative(copy(self.preactivations))

        weightDerivatives = self.errSignal * self.activations.Transpose()
        biasDerivatives = self.errSignal

        self.weightUpdates += weightDerivatives * lr
        self.biasUpdates += biasDerivatives * lr

    def UpdateWeightsAndBiases(self, epochCount): # Update Weights and Biases
        self.weightMatrix -= (self.weightUpdates * (1 / epochCount))
        self.biasVector -= (self.biasUpdates * (1 / epochCount))

        self.weightUpdates.Clear()
        self.biasUpdates.Clear()

class Experience(): # Used in Experience Replay
    def __init__(self, state = None, action = None, reward = None, stateNew = None): # Constructor for an Experience
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
        return self.queue[(self.frontP + 1) % self.length]

    def Sample(self, n): # Samples N number of samples from the deque
        temp = self.queue
        return random.sample(temp, n)