import random, pickle
from matrix import Matrix

class NeuralNet():
    def __init__(self, layers):
        self.layers = []

        self.layers.append()

    def ForwardPropagation(self, inputVector):
        pass

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