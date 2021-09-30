class MatExcepts():
    mismatchOrders = Exception("Orders of Matrices do not match")



class Matrix():
    # Init Function
    def __init__(self, arg1):
        if type(arg1) == list: # Passed in existing values
            self.matrixVals = arg1
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

        elif type(arg1) == tuple: # Passed in order of Matrix, creates a blank Matrix
            self.matrixVals = [[0 for i in range(arg1[1])] for j in range(arg1[0])]
            self.order = (len(self.matrixVals), len(self.matrixVals[0]))

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
        pass

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
    m1 = Matrix([[1, 2],[3, 4]])

    m2 = m1 + m1
    print(m2)

    m3 = m1 - m2
    print(m3)