from abc import ABC, abstractmethod
from math import e, tanh, exp, cosh
from matrix import *

class Activation(ABC): # Abstract Base Class
    @abstractmethod
    def Activation(self, x): # Abstract Activation Method
        pass

    @abstractmethod
    def Derivative(self, x): # Abstract Derivative Method
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
            if x.matrixVals[row][0] >= 0: x.matrixVals[row][0] = 1
            else: x.matrixVals[row][0] = 0
        return x

class LeakyReLu(Activation): # Leaky ReLu
    def __init__(self):
        pass

    def Activation(self, x): # Returns value if greater than 0, else a apply a gradient to x and return it
        for row in range(x.order[0]):
            x.matrixVals[row][0] = max(x.matrixVals[row][0] * 0.1, x.matrixVals[row][0])
        return x

    def Derivative(self, x): # If value is greater than 0 return 1, else return 0.01
        for row in range(x.order[0]):
            if x.matrixVals[row][0] >= 0: x.matrixVals[row][0] = 1
            else: x.matrixVals[row][0] = 0.1
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

    def Derivative(self, x): # Derivative of the Sigmoid Function
        for row in range(x.order[0]):
            sigmoidSingle = self.ActivationSingle(x.matrixVals[row][0])
            x.matrixVals[row][0] = sigmoidSingle * (1 - sigmoidSingle)
        return x

    def ActivationSingle(self, x): # Single value for use in the derivative
        if x > 15: return 1
        elif x < -15: return 0
        else: return 1 / (1 + exp(-x))

class SoftMax(Activation): # SoftMax
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        sumToK = 0

        for i in range(x.order[0]):
            sumToK += exp(x.matrixVals[i][0])

        outVector = Matrix(x.order)

        for i in range(x.order[0]):
            outVector.matrixVals[i][0] = (exp(x.matrixVals[i][0])) / sumToK

        return outVector # Returns vector and best index

    def Derivative(self, x): # Derivative of the softmax function
        for row in range(x.order[0]):
            x.matrixVals[row][0] = x.matrixVals[row][0] * (1 - x.matrixVals[row][0])
        
        return x

class NullActivation(Activation): # No activation function
    def __init__(self):
        pass

    def Activation(self, x): # Returns the same values
        return x

    def Derivative(self, x): # Returns the same values
        return 1

class TanH(Activation): # TanH
    def __init__(self):
        pass

    def Activation(self, x): # TanH mathematical function
        for row in range(x.order[0]):
            x.matrixVals[row][0] = tanh(x.matrixVals[row][0])
        return x

    def Derivative(self, x): # Derivative of TanH
        for row in range(x.order[0]):
            x.matrixVals[row][0] = (1 / (cosh(x.matrixVals[row][0]))) ** 2
        return x