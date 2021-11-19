import random, pickle, math
from matrix import Matrix
import activations
from copy import copy

class DoubleNeuralNet(): # Wraps a Main and Target Neural Network together
    def __init__(self, layers, params, load=False, loadName="DQNetwork"): # Constructor for a Double Neural Network
        self.paramDictionary = params

        if not load:
            self.MainNetwork = NeuralNet(layers, params)
            self.TargetNetwork = NeuralNet(layers, params)

            self.ExperienceReplay = Deque(self.paramDictionary["ERBuffer"])

            self.epsilon = self.paramDictionary["DQLEpsilon"]

            self.step = 0
            self.cumReward = 0.0
            
            self.layerActivation = activations.TanH()
            self.finalLayerActivation = activations.SoftMax()
        else:
            self.LoadState(loadName)

        self.fileName = loadName
        
        self.activations = (self.layerActivation, self.finalLayerActivation) # Tuple of activations

    def TakeStep(self, agent, worldMap, enemyList): # Takes a step forward in time
        self.step += 1

        # Forward Propagation
        agentSurround = agent.GetTileVector(worldMap, enemyList)
        postProcessedSurround = agent.TileVectorPostProcess(agentSurround) # Retrieve Vector of State info from Agent
        netInput = postProcessedSurround[1]
        
        self.MainNetwork.ForwardPropagation(netInput, self.activations) # Forward Prop the Main Network

        output = self.MainNetwork.layers[-1].outputVector
        outputMax = output.MaxInVector()

        # Action Taking and Reward
        if random.random() < self.epsilon: # Epsilon slowly regresses, leaving a greater chance for a random action to be explored
            if type(self.finalLayerActivation) == activations.Sigmoid:
                action = randint(0, 6)
                val = random.random()
                totalled = 0
                for i in range(output.order[0]):
                    totalled += output.matrixVals[i][0]
                    if totalled >= val:
                        action = i
                        break
            else:
                action = random.randint(0, 6)
        else:
            action = outputMax[1]


        #print(action)
        rewardVector = agent.GetRewardVector(agentSurround, self.paramDictionary["DeepQLearningLayers"][-1])
        reward = rewardVector.matrixVals[action][0] # Get reward given action
        print(rewardVector, action, reward)
        self.cumReward += reward

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
        LossVector = self.LossFunctionV2(output, tempExp, agent)
        self.MainNetwork.layers[-1].errSignal = LossVector

        self.MainNetwork.BackPropagationV2(self.activations)
        #print(output)

        # Do things every X steps passed
        if self.step % self.paramDictionary["TargetReplaceRate"] == 0: # Replace Weights in Target Network
            self.TargetNetwork.layers = self.MainNetwork.layers

        if (self.paramDictionary["EREnabled"] and self.step % self.paramDictionary["ERSampleRate"] == 0 and 
                                            self.ExperienceReplay.Full()):         # Sample Experience Replay Buffer
            self.SampleExperienceReplay(agent)

        if self.step % self.paramDictionary["DQLEpoch"] == 0:
            print(self.step, self.cumReward, self.epsilon)

            self.MainNetwork.UpdateWeightsAndBiases(self.paramDictionary["DQLEpoch"])

            if self.paramDictionary["SaveWeights"]:
                self.SaveState(self.fileName)

    def SampleExperienceReplay(self, agent): # Samples the Experience Replay Buffer, Back Propagating its Findings
        samples = self.ExperienceReplay.Sample(self.paramDictionary["ERSampleSize"])

        for sample in samples:
            postProcessedSurround = agent.TileVectorPostProcess(sample.state) # Post process the Tile Vector
            netInput = postProcessedSurround[1]

            self.MainNetwork.ForwardPropagation(netInput, self.activations) # Forward Prop the Main Network

            output = self.MainNetwork.layers[-1].outputVector

            Loss = self.LossFunctionV2(output, sample, agent)

            self.MainNetwork.BackPropagationV2(self.activations)

        print("Sampled")

    def LossFunctionV2(self, output, tempExp, agent):
        # L^i(W^i) = ((r + y*maxQ(s',a';W^i-1) - Q(s,a,W)) ** 2
        # Loss = ((Reward[] + Gamma * MaxQ(s', a'; TNet)) - Q(s, a)[]) ^ 2

        Reward = tempExp.reward
        Gamma = self.paramDictionary["DQLGamma"]

        stateNew = agent.TileVectorPostProcess(tempExp.stateNew)
        self.TargetNetwork.ForwardPropagation(stateNew[1], self.activations)
        tempRewardVec = agent.GetRewardVector(tempExp.stateNew, self.paramDictionary["DeepQLearningLayers"][-1])
        maxQTNet = agent.MaxQ(tempRewardVec)

        #print(Reward.order, output.order)
        LossVec = ((Reward + (Gamma * maxQTNet)) - output) ** 2
        return LossVec

    def SaveNetworks(self):
        self.MainNetwork.SaveNeuralNet("MainNetwork")
        self.TargetNetwork.SaveNeuralNet("TargetNetwork")

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

        self.layers = []

        for i in range(len(layersIn)):
            if i == 0:
                self.layers.append(Layer(0, layersIn[0], True))
            else:
                self.layers.append(Layer(layersIn[i - 1], layersIn[i]))

    def ForwardPropagation(self, inputVector, activations): # Iterates through Forward Propagation
        self.layers[0].outputVector = inputVector

        for i in range(1, len(self.layers) - 1):
            self.layers[i].ForwardPropagation(self.layers[i-1], activations)

        self.layers[-1].ForwardPropagation(self.layers[-2], activations, finalLayer=True)

    def BackPropagationV2(self, activations): # Iterates through Back Propagation V2
        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i].BackPropagationV2(self.layers[i-1], self.paramDictionary["DQLLearningRate"], activations)

    def UpdateWeightsAndBiases(self, epochCount):
        for i in range(1, len(self.layers) - 1):
            self.layers[i].UpdateWeightsAndBiases(epochCount)

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

            self.weightUpdates = Matrix((size, prevSize))

            self.biasUpdates = Matrix((size, 1))

        self.errSignal = Matrix((size, 1))
        
        self.sVector = Matrix((size, 1))
        self.outputVector = Matrix((size, 1))

    def ForwardPropagation(self, prevLayer, activations, finalLayer=False): # Forward Propagates the Neural Network
        weightValueProduct = self.weightMatrix * prevLayer.outputVector

        self.sVector = weightValueProduct + self.biasVector

        if not finalLayer:
            self.outputVector = activations[0].Activation(self.sVector)
        else:
            self.outputVector = activations[1].Activation(self.sVector)

    def BackPropagationV2(self, prevLayer, lr, layerActivations, finalLayer=False): # 2nd Revision of Back Propagation
        # Calculating Next Error Signal
        halfErrSignal = (self.weightMatrix.Transpose() * self.errSignal)

        zDerivative = layerActivations[0].Derivative(prevLayer.sVector) # Applying derivative functions to the output of a layerN

        errSignal = halfErrSignal * zDerivative # Hadamard Product to get error signal for previous layer
        prevLayer.errSignal = errSignal

        # Calculating Weight updates
        updatedWeightVectors = []
        for delta in range(self.errSignal.order[0]):
            errSignal = self.errSignal.matrixVals[delta][0]

            selectedColumn = self.weightMatrix.Transpose().SelectColumn(delta)
            updatedWeightVectors.append(selectedColumn * errSignal * (-lr))

        # Combining the weight updates into a matrix and adding it to the weight updates Matrix
        self.weightUpdates += Matrix.CombineVectorsHor(updatedWeightVectors).Transpose()

        self.biasUpdates += self.errSignal * lr # Bias Updates

    def UpdateWeightsAndBiases(self, epochCount):
        self.weightMatrix += self.weightUpdates * (1 / epochCount)
        self.biasVector -= self.biasUpdates * (1 / epochCount)

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