from abc import ABC, abstractmethod
from math import e, tanh

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

    def Activation(self, x):
        return 1 / (1 + math.exp(-x))

    def Derivative(self, x):
        sigmoidX = self.Activation(x)
        return sigmoidX * (1 - sigmoidX)

class SoftMax(Activation): # SoftMax
    def __init__(self):
        pass

    def Activation(self, x): # Returns a probability distribution between a vector of values totalling to 1
        pass

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