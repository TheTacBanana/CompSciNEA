class MatExcepts():
    mismatchOrders = Exception("Orders of Matrices do not match")
    unableToCreateIdentityMat = Exception("Unable to create identity Matrix from given arguments")

class Matrix():
    # Init Function
    def __init__(self, arg1, identity=False, random=False):
        if type(arg1) == list: # Passed in existing values
            self.matrixVals = arg1
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        elif type(arg1) == tuple: # Passed in order of Matrix, creates a blank Matrix
            self.matrixVals = [[0 for i in range(arg1[1])] for j in range(arg1[0])]
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        #Key Arguments
        if identity == True:
            if self.order[0] == self.order[1] and type(arg1) == tuple:
                for i in range(self.order[0]):
                    self.matrixVals[i][i] = 1
            else:
                raise MatExcepts.unableToCreateIdentityMat
        if random == True:
            for row in range(self.order[0]):
                for col in range(self.order[1]):
                    self.matrixVals[row][col] = (random.random() - 0.5) * 2

    # Overloading Addition Operator
    def __add__(self, m2):
        if self.order != m2.order:
            raise MatExcepts.mismatchOrders

        tempMatrix = Matrix(self.order)

        for row in range(self.order[0]):
            for col in range(self.order[1]):
                tempMatrix.matrixVals[row][col] = self.matrixVals[row][col] + m2.matrixVals[row][col]

        return tempMatrix

    # Overloading Subtraction Operator
    def __sub__(self, m2):
        if self.order != m2.order:
            raise MatExcepts.mismatchOrders

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

        elif type(m2) == Matrix: # Matrix Multiplication
            if self.order[0] != m2.order[1]:
                raise MatExcepts.mismatchOrders
            tempMatrix = Matrix((self.order[0], m2.order[1]))

            cumProduct = 0
            for row in range(self.order[0]): # For row in M1
                for col in range(m2.order[1]): # For column in M2
                    for subColRow in range(self.order[1]): # For element in column in M2
                        cumProduct += self.matrixVals[row][subColRow] * m2.matrixVals[subColRow][col]
                    tempMatrix.matrixVals[row][col] = cumProduct
                    cumProduct = 0
            return tempMatrix        

    # Overloading convert to string method
    def __str__(self):
        strOut = ""
        for row in range(self.order[0]):
            if row != self.order[0] - 1:
                strOut += str(self.matrixVals[row]) + "\n"
            else:
                strOut += str(self.matrixVals[row])
        return strOut

class MatrixTest():
    pass
    m1 = Matrix([[1, 2],[3, 4]])
    m2 = Matrix([[1, 2]])

    m4 = m1 * m1
    #print(m4)

    m3 = m2 - m2
    #print(m3)