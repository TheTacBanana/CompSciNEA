import random as rnd
class MatExcepts(): # Exception class to avoid repeating same exception
    NoMatchingInitCase = Exception("No Matching Init case for given parameters")
    MismatchOrders = Exception("Orders of Matrices do not match")
    UnableToCreateIdentityMat = Exception("Unable to create identity Matrix from given arguments")
    UnableToMultiply = Exception("No matching multiply case found")
    ColumnOutOfRange = Exception("Specified Column out of range of Matrix")
    ColumnMustBeInteger = Exception("Specified Column must be of type Integer")
    RowOutOfRange = Exception("Specified Row out of range of Matrix")
    RowMustBeInteger = Exception("Specified Row must be of type Integer")
    NotOfTypeVector = Exception("1 or more 'Vectors' aren't Vectors")
    VectorsNotOfSameLength = Exception("Given list of vectors isnt all same height")

class Matrix():
    # Init Function
    def __init__(self, arg1, identity=False, random=False):
        if type(arg1) == list: # Passed in existing values
            self.matrixVals = arg1
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        elif type(arg1) == tuple: # Passed in order of Matrix, creates a blank Matrix
            self.matrixVals = [[0 for i in range(arg1[1])] for j in range(arg1[0])]
            #print(arg1)
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))
        else:
            raise MatExcepts.NoMatchingInitCase

        #Key Arguments
        if identity == True: # Creates Identity Matrix
            if self.order[0] == self.order[1] and type(arg1) == tuple:
                for i in range(self.order[0]):
                    self.matrixVals[i][i] = 1
            else:
                raise MatExcepts.UnableToCreateIdentityMat

        if random == True: # Initiation random values between -0.5 and 0.5
            for row in range(self.order[0]):
                for col in range(self.order[1]):
                    self.matrixVals[row][col] = (rnd.random() - 0.5) 

    # Overloading Addition Operator
    def __add__(self, m2):
        if self.order != m2.order:
            raise MatExcepts.MismatchOrders

        tempMatrix = Matrix(self.order)

        for row in range(self.order[0]):
            for col in range(self.order[1]):
                tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] + m2.matrixVals[row][col]

        return tempMatrix

    # Overloading Subtraction Operator
    def __sub__(self, m2):
        if self.order != m2.order:
            raise MatExcepts.MismatchOrders

        tempMatrix = Matrix(self.order)

        for row in range(self.order[0]):
            for col in range(self.order[1]):
                tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] - m2.matrixVals[row][col]

        return tempMatrix

    # Overloading Multiplication Operator
    def __mul__(self, m2):
        if type(m2) == float or type(m2) == int: # Scalar Multiply
            for row in range(self.order[0]):
                for col in range(self.order[1]):
                    self.matrixVals[row][col] = self.matrixVals[row][col] * m2
            return self

        elif self.order[1] == 1 and m2.order[1] == 1 and self.order[0] == m2.order[0]: # Hadamard product between two vectors
            for row in range(self.order[0]):
                self.matrixVals[row][0] *= m2.matrixVals[row][0]
            return self

        elif type(m2) == Matrix: # Matrix Multiplication
            if self.order[1] != m2.order[0]:
                raise MatExcepts.MismatchOrders
            tempMatrix = Matrix((self.order[0], m2.order[1]))

            cumProduct = 0
            for row in range(self.order[0]): # For row in M1
                for col in range(m2.order[1]): # For column in M2
                    for subColRow in range(self.order[1]): # For element in column in M2
                        cumProduct += self.matrixVals[row][subColRow] * m2.matrixVals[subColRow][col]
                    tempMatrix.matrixVals[row][col] = cumProduct
                    cumProduct = 0
            return tempMatrix
        else:
            raise MatExcepts.UnableToMultiply

    # Overloading convert to string method
    def __str__(self): # Printing to console nicely and easily
        strOut = ""
        for row in range(self.order[0]):
            if row != self.order[0] - 1:
                strOut += str(self.matrixVals[row]) + "\n"
            else:
                strOut += str(self.matrixVals[row])
        return strOut

    # Reflects matrix across the diagonal
    def Transpose(self):
        tempMatrix = Matrix((self.order[1], self.order[0]))
        
        for row in range(self.order[0]):
            for col in range(self.order[1]):
                tempMatrix.matrixVals[col][row] = self.matrixVals[row][col]
        return tempMatrix

    # Selects a column from the given Matrix
    def SelectColumn(self, column):
        if column < 0 or column > self.order[1] - 1:
            raise MatExcepts.ColumnOutOfRange

        if type(column) != int:
            raise MatExcepts.ColumnMustBeInteger

        tempMatrix = Matrix((self.order[0], 1))
        for row in range(self.order[0]):
            tempMatrix.matrixVals[row][0] = self.matrixVals[row][column]
        return tempMatrix

    # Select a row from the given Matrix
    def SelectRow(self, row):
        if type(row) != int:
            raise MatExcepts.RowMustBeInteger
        if column < 0 or column > self.order[1] - 1:
            raise MatExcepts.RowOutOfRange

        newMat = Matrix(self.matrixVals[row])

    @staticmethod
    def CombineVectorsHor(vectorList): # Concatenates a list of vectors into a singular matrice horizontally
        firstHeight = vectorList[0].order[0]
        for vec in vectorList:
            if vec.order[0] != firstHeight:
                raise MatExcepts.VectorsNotOfSameLength
            if vec.order[1] != 1:
                raise MatExcepts.NotOfTypeVector

        tempMatrix = Matrix((vectorList[0].order[0], len(vectorList)))
        for col in range(tempMatrix.order[1]):
            for row in range(tempMatrix.order[0]):
                tempMatrix.matrixVals[row][col] = vectorList[col].matrixVals[row][0]
        return tempMatrix