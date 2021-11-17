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
        return max(0, x)

    def Derivative(self, x): # If value is greater than 0 return 1, else return 0
        if x > 0:
            return 1
        else:
            return 0

class LeakyReLu(Activation): # Leaky ReLu
    def __init__(self):
        pass

    def Activation(self, x): # Returns value if greater than 0, else a apply a gradient to x and return it
        return max(0.01 *  x, x)

    def Derivative(self, x): # If value is greater than 0 return 1, else return 0.01
        if x > 0:
            return 1
        else:
            return 0.01

class Sigmoid(Activation): # Sigmoid
    def __init__(self):
        pass

    def Activation(self, x): # Mathematical Function to get "squish" values between 0 and 1
        if x > 10:
            return 1
        elif x < -10:
            return 0
        else:
            return 1 / (1 + exp(-x))

    def Derivative(self, x):
        sigmoidX = self.Activation(x)
        return sigmoidX * (1 - sigmoidX)

class SoftMax(Activation): # SoftMax
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        sumToK = 0
        maxIndex = 0

        for i in range(x.order[0]):
            sumToK += exp(x.matrixVals[i][0])

            if x.matrixVals[i][0] > x.matrixVals[maxIndex][0]:
                maxIndex = i

        outVector = Matrix(x.order)

        for i in range(x.order[0]):
            outVector.matrixVals[i][0] = (exp(x.matrixVals[i][0])) / sumToK

        maxVal = outVector.matrixVals[maxIndex][0]

        return outVector, maxIndex, maxVal # Returns vector and best index

    def Derivative(self, x): 
        pass

class TanH(Activation): # TanH
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        return tanh(x)

    def Derivative(self, x): 
        temp =  tanh(x)
        return 1 - (temp ** 2)