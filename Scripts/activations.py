from abc import ABC, abstractmethod
from math import e, tanh, exp
from matrix import *

class Activation(ABC): # Abstract Base Class
    @abstractmethod
    def Activation(self, x):
        pass

    @abstractmethod
    def Derivative(self, x):
        pass

class ReLu(Activation): # ReLu
    def __init__(self):
        pass

    def Activation(self, x): # Returns value if greater than 0, else 0
        for row in range(x.order[0]):
            x.matrixVals[row][0] = max(0, x.matrixVals[row][0])
        return x

    def Derivative(self, x): # If value is greater than 0 return 1, else return 0
        for row in range(x.order[0]):
            if x.matrixVals[row][0] > 0: x.matrixVals[row][0] = 1
            else: 0
        return x

class LeakyReLu(Activation): # Leaky ReLu
    def __init__(self):
        pass

    def Activation(self, x): # Returns value if greater than 0, else a apply a gradient to x and return it
        for row in range(x.order[0]):
            x.matrixVals[row][0] = max(x.matrixVals[row][0] * 0.01, x.matrixVals[row][0])
        return x

    def Derivative(self, x): # If value is greater than 0 return 1, else return 0.01
        for row in range(x.order[0]):
            if x.matrixVals[row][0] > 0: x.matrixVals[row][0] = 1
            else: 0.1
        return x

class Sigmoid(Activation): # Sigmoid
    def __init__(self):
        pass

    def Activation(self, x): # Mathematical Function to get "squish" values between 0 and 1
        for row in range(x.order[0]):
            if x.matrixVals[row][0] > 15: x.matrixVals[row][0] = 1
            elif x.matrixVals[row][0] < -15: x.matrixVals[row][0] = 0
            else: x.matrixVals[row][0] = 1 / (1 + exp(-x.matrixVals[row][0]))
        return x

    def Derivative(self, x):
        for row in range(x.order[0]):
            sigmoidSingle = self.ActivationSingle(x.matrixVals[row][0])
            x.matrixVals[row][0] = sigmoidSingle * (1 - sigmoidSingle)
        return x

    def ActivationSingle(self, x):
        if x > 15: return 1
        elif x < -15: return 0
        else: return 1 / (1 + exp(-x))

class SoftMax(Activation): # SoftMax
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        sumToK = 0
        #maxIndex = 0

        for i in range(x.order[0]):
            sumToK += exp(x.matrixVals[i][0])

            #if x.matrixVals[i][0] > x.matrixVals[maxIndex][0]:
            #    maxIndex = i

        outVector = Matrix(x.order)

        for i in range(x.order[0]):
            outVector.matrixVals[i][0] = (exp(x.matrixVals[i][0])) / sumToK

        #maxVal = outVector.matrixVals[maxIndex][0]

        return outVector # Returns vector and best index

    def Derivative(self, x): 
        xNew = x
        for row in range(xNew.order[0]):
            xNew.matrixVals[row][0] = 1 - x.matrixVals[row][0]
        
        return x * xNew

class NullActivation(Activation):
    def __init__(self):
        pass

    def Activation(self, x): # Returns the same values
        return x

    def Derivative(self, x): # Returns the same values
        return x

class TanH(Activation): # TanH
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        for row in range(x.order[0]):
            x.matrixVals[row][0] = tanh(x.matrixVals[row][0])
        return x

    def Derivative(self, x): 
        for row in range(x.order[0]):
            x.matrixVals[row][0] = 1 - (tanh(x.matrixVals[row][0]) ** 2)
        return x