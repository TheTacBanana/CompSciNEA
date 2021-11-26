from matrix import *
from random import randint, seed

class MatrixTest():
    def __init__(self, seedIn):
        seed(seedIn)

        self.ConstructorTests = {"CreateVectorFrom1DList": False,
                                 "CreateMatrixFrom2DList": False,
                                 "CreateMatrixFromTuple": False,
                                 "CreateIdentityMatrix": False}

        self.ConstructorExceptions = {"NoMatchingInitCase": False,
                                      "UnableToCreateIdentityMat": False}

        self.MethodUnitsTests = {"Addition": False,
                               "Subtraction": False,
                               "Multiplication": False,
                               "Power": False,
                               "Transpose": False,
                               "SelectColumn": False,
                               "SelectColumn": False,
                               "SelectRow": False,
                               "Sum": False,
                               "MaxInVector": False,
                               "Clear": False,
                               "CombineVectorsHor": False}

        self.MethodExceptions = {"NoMatchingMultiplycase": False,
                               "NoMatchingAdditionCase": False,
                               "NoMatchingSubtractionCase": False,
                               "NoMatchingPowerCase": False,
                               "MismatchOrders": False,
                               "SumOfMatrixReqNumericalVals": False,
                               "ColumnOutOfRange": False,
                               "ColumnMustBeInteger": False,
                               "RowOutOfRange": False,
                               "RowMustBeInteger": False,
                               "NotOfTypeVector": False,
                               "VectorsNotOfSameLength": False}

    def RunAllTests(self):
        self.ConstructorTest()
        self.ConstructorExceptionsTest()
        self.MethodUnitTest()
        self.MethodException()

        self.TestingResults()

# Constructor Tests
    def ConstructorTest(self):
        print(self.CreateVectorFrom1DList())
        print(self.CreateMatrixFrom2DList())
        print(self.CreateMatrixFromTuple())
        print(self.CreateIdentityMatrix())

    def CreateVectorFrom1DList(self): # Finished
        result = True
        vals = [randint(-10, 10) for i in range(randint(3, 10))]
        v1 = Matrix(vals)

        if v1.order[0] != len(vals) or v1.order[1] != 1:
            result = False

        for i in range(len(vals)):
            if vals[i] != v1.matrixVals[i][0]:
                result = False

        return result
    def CreateMatrixFrom2DList(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        m1 = Matrix(vals)

        if m1.order[0] != 2 or m1.order[1] != 2:
            result = False
        if m1.matrixVals != vals:
            result = False 

        return result
    def CreateMatrixFromTuple(self): # Finished
        result = True
        order = (randint(1, 10), randint(1, 10))

        m1 = Matrix(order)
        if m1.order != order:
            result = False

        for row in range(m1.order[0]):
            for col in range(m1.order[1]):
                if m1.matrixVals[row][col] != 0:
                    result = False

        return result
    def CreateIdentityMatrix(self): # Finished
        result = True
        rand = randint(1, 10)
        order = ((rand, rand))

        m1 = Matrix(order, identity=True)
        if m1.order != order:
            result = False

        for row in range(m1.order[0]):
            for col in range(m1.order[1]):
                if row == col:
                    if m1.matrixVals[row][col] != 1:
                        result = False

                elif m1.matrixVals[row][col] != 0:
                    result = False

        return result

# Constructor Exception Tests
    def ConstructorExceptionsTest(self):
        print(self.NoMatchingInitCase())
        print(self.UnableToCreateIdentityMat())

    def NoMatchingInitCase(self): # Finished
        try:
            m1 = Matrix(1)
            return False
        except Exception as x:
            if x == MatExcepts.NoMatchingInitCase: return True
            else: return False
    def UnableToCreateIdentityMat(self): # Finished
        try:
            rand = randint(1, 10)
            m1 = Matrix((rand, rand + 1), identity=True)
            return False
        except Exception as x:
            if x == MatExcepts.UnableToCreateIdentityMat: return True
            else: return False

# Method Unit Tests
    def MethodUnitTest(self):
        print(self.AdditionMatrix())
        print(self.AdditionInteger())
        print(self.SubtractionMatrix())
        print(self.SubtractionInteger())
        print(self.MultiplicationInteger())
        print(self.MultiplicationHadamardVector())

    def AdditionMatrix(self): # Finished
        result = True
        vals1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        vals2 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = [[vals1[0][0] + vals2[0][0], vals1[0][1] + vals2[0][1]],
                     [vals1[1][0] + vals2[1][0], vals1[1][1] + vals2[1][1]]]

        m1 = Matrix(vals1)
        m2 = Matrix(vals2)
        m3 = m1 + m2

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def AdditionInteger(self): # Finished
        result = True
        vals1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valInt = randint(-10, 10)
        valsResult = [[vals1[0][0] + valInt, vals1[0][1] + valInt],
                     [vals1[1][0] + valInt, vals1[1][1] + valInt]]

        m1 = Matrix(vals1)
        m3 = m1 + valInt

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def SubtractionMatrix(self): # Finished
        result = True
        vals1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        vals2 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = [[vals1[0][0] - vals2[0][0], vals1[0][1] - vals2[0][1]],
                     [vals1[1][0] - vals2[1][0], vals1[1][1] - vals2[1][1]]]

        m1 = Matrix(vals1)
        m2 = Matrix(vals2)
        m3 = m1 - m2

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def SubtractionInteger(self): # Finished
        result = True
        vals1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valInt = randint(-10, 10)
        valsResult = [[vals1[0][0] - valInt, vals1[0][1] - valInt],
                     [vals1[1][0] - valInt, vals1[1][1] - valInt]]

        m1 = Matrix(vals1)
        m3 = m1 - valInt

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def MultiplicationInteger(self): # Finished
        result = True
        vals1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valInt = randint(-10, 10)
        valsResult = [[vals1[0][0] * valInt, vals1[0][1] * valInt],
                     [vals1[1][0] * valInt, vals1[1][1] * valInt]]

        m1 = Matrix(vals1)
        m3 = m1 * valInt

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def MultiplicationHadamardVector(self): # Finished
        result = True

        cols = randint(3, 10)
        vals1 = [randint(-10, 10) for i in range(cols)]
        vals2 = [randint(-10, 10) for i in range(cols)]
        valsResult = [[vals1[i] * vals2[i]] for i in range(cols)]

        v1 = Matrix(vals1)
        v2 = Matrix(vals2)
        v3 = v1 * v2

        if v3.matrixVals != valsResult:
            result = False

        return result
    def MultiplicationMatrix(self):
        pass

    def Power(self):
        pass

    def Transpose(self):
        pass

    def SelectColumn(self):
        pass

    def SelectRow(self):
        pass

    def CombineVectorHorizontal(self):
        pass

# Method Exception Tests
    def MethodException(self):
        pass

    def TestingResults(self):
        pass

MT = MatrixTest(0)
MT.RunAllTests()