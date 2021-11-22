import random as rnd
class MatExcepts(): # Exception class to avoid repeating same exception
    # Constructor Errors
    NoMatchingInitCase =            Exception("No Matching Init case for given parameters")
    UnableToCreateIdentityMat =     Exception("Unable to create identity Matrix from given arguments")

    # Vector Errors
    NotOfTypeVector =               Exception("Given list of Vectors contains a Matrix")
    VectorsNotOfSameLength =        Exception("All Vectors must be the same height")
    
    # Operation Errors
    NoMatchingMultiplycase =        Exception("No matching multiply case found")
    NoMatchingAdditionCase =        Exception("No matching addition case found")
    NoMatchingSubtractionCase =     Exception("No matching addition case found")
    NoMatchingPowerCase =           Exception("No matching power case was found")
    MismatchOrders =                Exception("Orders of Matrices do not match")
    SumOfMatrixReqNumericalVals =   Exception("The sum of a Matrix requires Numerical values to be populated")

    # Select Row/Column Errors
    ColumnOutOfRange =              Exception("Specified Column out of range of Matrix")
    ColumnMustBeInteger =           Exception("Specified Column must be of type Integer")
    RowOutOfRange =                 Exception("Specified Row out of range of Matrix")
    RowMustBeInteger =              Exception("Specified Row must be of type Integer")

class Matrix():
    # Init Function
    def __init__(self, arg1, identity=False, random=False):
        if type(arg1) == list: # Passed in existing values
            if type(arg1[0]) != list: # Create Vector when 1d List passed in
                self.matrixVals = [[0] for j in range(len(arg1))] # List Comprehension to populate 2d array of 0's

                for row in range(len(arg1)): # Populates 2d list from 1d list
                    self.matrixVals[row][0] = arg1[row]
                    self.order = (len(self.matrixVals), len(self.matrixVals[0]))

            else: # Create Matrix from 2d List
                self.matrixVals = arg1
                self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        elif type(arg1) == tuple: # Passed in order of Matrix, creates a blank Matrix
            self.matrixVals = [[0 for column in range(arg1[1])] for row in range(arg1[0])] # List Comprehension to populate 2d array of 0's
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        else: # No matching Constructor case so throw error
            raise MatExcepts.NoMatchingInitCase

        #Key Arguments
        if identity == True: # Creates Identity Matrix
            if self.order[0] == self.order[1] and type(arg1) == tuple:
                for pos in range(self.order[0]): # Populate matrix along the diagonal
                    self.matrixVals[pos][pos] = 1
            else:
                raise MatExcepts.UnableToCreateIdentityMat

        if random == True: # Initiation random values between -0.5 and 0.5
            for row in range(self.order[0]):
                for col in range(self.order[1]):
                    self.matrixVals[row][col] = (rnd.random() - 0.5)

    # Overloading Addition Operator
    def __add__(self, m2):
        if type(m2) == Matrix: # Add 2 Matrices together 
            if self.order != m2.order: # Throw error if orders dont match
                raise MatExcepts.MismatchOrders

            tempMatrix = Matrix(self.order) # Create new temporary matrix to populate with new values

            for row in range(self.order[0]): # Populate values
                for col in range(self.order[1]):
                    tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] + m2.matrixVals[row][col]

            return tempMatrix # Return temporary matrix

        elif type(m2) == float or type(m2) == int: # Add value to each element in Matrix
            tempMatrix = Matrix(self.order)

            for row in range(self.order[0]): # Apply operation
                for col in range(self.order[1]):
                    tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] + m2

            return tempMatrix

        else: # Throw error if no matching cases found
            raise MatExcepts.NoMatchingAdditionCase 

    # Overloading Subtraction Operator
    def __sub__(self, m2):
        if type(m2) == Matrix:
            if self.order != m2.order: # Throw error if orders dont match
                raise MatExcepts.MismatchOrders

            tempMatrix = Matrix(self.order) # Create Temporary Matrix to populate with values

            for row in range(self.order[0]): # Populate values
                for col in range(self.order[1]):
                    tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] - m2.matrixVals[row][col]

            return tempMatrix # Return temporary Matrix

        elif type(m2) == float or type(m2) == int: # Subract value from each element in Matrix
            tempMatrix = Matrix(self.order)

            for row in range(self.order[0]): # Apply operation
                for col in range(self.order[1]):
                    tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] + m2

            return tempMatrix # Return temporary Matrix

        else: # Throw error if no matching cases found
            raise MatExcepts.NoMatchingSubtractionCase

    # Overloading Multiplication Operator
    def __mul__(self, m2):
        if type(m2) == float or type(m2) == int: # Scalar Multiply
            tempMatrix = Matrix(self.order) # Create Temporary Matrix

            for row in range(self.order[0]):
                for col in range(self.order[1]):
                    tempMatrix.matrixVals[row][0] = self.matrixVals[row][0] * m2 # Apply Operation 
            return self

        elif self.order[1] == 1 and m2.order[1] == 1 and self.order[0] == m2.order[0]: # Hadamard product between two vectors
            tempMatrix = Matrix(self.order) # Create Temporary Matrix

            for row in range(self.order[0]):
                tempMatrix.matrixVals[row][0] = self.matrixVals[row][0] * m2.matrixVals[row][0] # Apply Operation
            return self

        elif type(m2) == Matrix: # Matrix Multiplication
            if self.order[1] != m2.order[0]: # Throw error if orders are not the same
                raise MatExcepts.MismatchOrders

            tempMatrix = Matrix((self.order[0], m2.order[1])) # Create Temporary Matrix

            cumProduct = 0 # Cumulative product of row <-> column operations

            for row in range(self.order[0]): 
                for col in range(m2.order[1]): 
                    for subColRow in range(self.order[1]): # Sum the product between M1 Row and M2 Column
                        cumProduct += self.matrixVals[row][subColRow] * m2.matrixVals[subColRow][col] 
                    tempMatrix.matrixVals[row][col] = cumProduct # Apply to new matrix
                    cumProduct = 0
            return tempMatrix

        else: # Throw error if no matching cases found
            raise MatExcepts.NoMatchingMultiplycase

    # Overloading the Power Operator
    def __pow__(self, power):
        if type(m2) == int: 
            newMat = self # Create new Matrix from self

            for iterate in range(power - 1):
                newMat = self * newMat # Multiply new Matrix by self

            return newMat # Return New Matrix

        else: # Throw error if not integer value
            raise MatExcepts.NoMatchingPowerCase 

    # Overloading convert to string method
    def __str__(self): # Printing to console nicely and easily
        strOut = "" # Create empty string

        for row in range(self.order[0]): # Iterate through all values in matrix and add them to strOut
            strOut += str([str(self.matrixVals[row][col]) for col in range(self.order[1])]) + "\n"

        return strOut # Return strOut

    # Reflects matrix across the diagonal
    def Transpose(self):
        tempMatrix = Matrix((self.order[1], self.order[0])) # Create Temporary with reversed orders
        
        for row in range(self.order[0]):
            for col in range(self.order[1]):
                tempMatrix.matrixVals[col][row] = self.matrixVals[row][col] # Flipped row and column to create Transpose
        return tempMatrix

    # Selects a column from the given Matrix
    def SelectColumn(self, column):
        if column < 0 or column > self.order[1] - 1: # Throw exception if column is out of range
            raise MatExcepts.ColumnOutOfRange

        if type(column) != int: # Throw error if value isnt of type Integer
            raise MatExcepts.ColumnMustBeInteger

        tempMatrix = Matrix((self.order[0], 1)) # Create Temporary Matrix 

        for row in range(self.order[0]): # Iterate throw Matrix and assign to new Matrix
            tempMatrix.matrixVals[row][0] = self.matrixVals[row][column]

        return tempMatrix # Return Temporary Matrix

    # Select a row as list from the given Matrix
    def SelectRow(self, row):
        if type(row) != int: # Throw error if value isnt of type Integer
            raise MatExcepts.RowMustBeInteger
            
        if column < 0 or column > self.order[1] - 1: # Throw error if row out of range
            raise MatExcepts.RowOutOfRange

        newMat = self.matrixVals[row] 

        return newMat 

    # Sum of values in a Matrix
    def Sum(self):
        if type(self.matrixVals[0][0]) != int or type(self.matrixVals[0][0]) != float: # Throw error if not a numerical type
            raise MatExcepts.SumOfMatrixReqNumericalVals

        matSum = 0

        for col in range(tempMatrix.order[1]):
            for row in range(tempMatrix.order[0]):
                matSum += self.matrixVals[row][col] # Add value to matSum

        return matSum

    # Get Max item in Vector
    def MaxInVector(self):
        values = [self.matrixVals[row][0] for row in range(self.order[0])] # Uses List comprehension to form 1d list from Matrix values

        return max(values), max(range(len(values)), key=values.__getitem__) # Returns maximum element from the previously created list

    # Clear Matrix of values
    def Clear(self):
        self.matrixVals = [[0 for column in range(self.order[1])] for row in range(self.order[0])] # Sets all values in Matrix to 0

    # Concatenates a list of vectors into a singular matrice horizontally - Static method
    @staticmethod
    def CombineVectorsHor(vectorList): 
        firstHeight = vectorList[0].order[0]

        for vec in vectorList: # Iterates through vectorList to check they match the requirements, if not throws Error
            if vec.order[0] != firstHeight:
                raise MatExcepts.VectorsNotOfSameLength
            if vec.order[1] != 1:
                raise MatExcepts.NotOfTypeVector

        tempMatrix = Matrix((vectorList[0].order[0], len(vectorList))) # Create temporary Matrix

        for col in range(tempMatrix.order[1]):
            for row in range(tempMatrix.order[0]):
                tempMatrix.matrixVals[row][col] = vectorList[col].matrixVals[row][0] # Merge Vectors into 1 matrix

        return tempMatrix # Return temporary Matrix