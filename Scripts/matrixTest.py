from matrix import *
from random import randint, seed

class MatrixTest():
    def __init__(self, seedIn, testCount):
        seed(seedIn)

        self.testCount = testCount

        self.testResults = {}

    def RunAllTests(self):
        self.ConstructorTest()
        self.ConstructorExceptionsTest()
        self.MethodUnitTest()
        self.MethodException()

        self.TestingResults()

# Constructor Tests
    def ConstructorTest(self):
        self.testResults["CreateVectorFrom1DList"] = [self.CreateVectorFrom1DList() for i in range(self.testCount)]
        self.testResults["CreateMatrixFrom2DList"] = [self.CreateMatrixFrom2DList() for i in range(self.testCount)]
        self.testResults["CreateMatrixFromTuple"] = [self.CreateMatrixFromTuple() for i in range(self.testCount)]
        self.testResults["CreateIdentityMatrix"] = [self.CreateIdentityMatrix() for i in range(self.testCount)]

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
        self.testResults["NoMatchingInitCase"] = [self.NoMatchingInitCase() for i in range(self.testCount)]
        self.testResults["UnableToCreateIdentityMat"] = [self.UnableToCreateIdentityMat() for i in range(self.testCount)]

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
        self.testResults["AdditionMatrix"] = [self.AdditionMatrix() for i in range(self.testCount)]
        self.testResults["AdditionInteger"] = [self.AdditionInteger() for i in range(self.testCount)]
        self.testResults["SubtractionMatrix"] = [self.SubtractionMatrix() for i in range(self.testCount)]
        self.testResults["SubtractionInteger"] = [self.SubtractionInteger() for i in range(self.testCount)]
        self.testResults["MultiplicationInteger"] = [self.MultiplicationInteger() for i in range(self.testCount)]
        self.testResults["MultiplicationHadamardVector"] = [self.MultiplicationHadamardVector() for i in range(self.testCount)]
        self.testResults["MultiplicationMatrix"] = [self.MultiplicationMatrix() for i in range(self.testCount)]
        self.testResults["Power"] = [self.Power() for i in range(self.testCount)]
        self.testResults["Transpose"] = [self.Transpose() for i in range(self.testCount)]
        self.testResults["SelectColumn"] = [self.SelectColumn() for i in range(self.testCount)]
        self.testResults["SelectRow"] = [self.SelectRow() for i in range(self.testCount)]
        self.testResults["CombineVectorHorizontal"] = [self.CombineVectorHorizontal() for i in range(self.testCount)]
        self.testResults["Sum"] = [self.Sum() for i in range(self.testCount)]
        self.testResults["MaxInVector"] = [self.MaxInVector() for i in range(self.testCount)]
        self.testResults["Clear"] = [self.Clear() for i in range(self.testCount)]

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
    def MultiplicationMatrix(self): # Finished
        result = True
        v1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        v2 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = [[v1[0][0] * v2[0][0] + v1[0][1] * v2[1][0], v1[0][0] * v2[0][1] + v1[0][1] * v2[1][1]],
                     [v1[1][0] * v2[0][0] + v1[1][1] * v2[1][0], v1[1][0] * v2[0][1] + v1[1][1] * v2[1][1]]]

        m1 = Matrix(v1)
        m2 = Matrix(v2)
        m3 = m1 * m2

        if m3.matrixVals != valsResult:
            result = False 

        return result
    def Power(self): # Finished
        result = True
        v1 = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        v2 = v1
        valsResult = [[v1[0][0] * v2[0][0] + v1[0][1] * v2[1][0], v1[0][0] * v2[0][1] + v1[0][1] * v2[1][1]],
                     [v1[1][0] * v2[0][0] + v1[1][1] * v2[1][0], v1[1][0] * v2[0][1] + v1[1][1] * v2[1][1]]]

        m1 = Matrix(v1)
        m2 = m1 ** 2

        if m2.matrixVals != valsResult:
            result = False 

        return result
    def Transpose(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = [[vals[0][0], vals[1][0]],
                     [vals[0][1], vals[1][1]]]

        m1 = Matrix(vals)
        m2 = m1.Transpose()

        if m2.matrixVals != valsResult:
            result = False 

        return result
    def SelectColumn(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult1 = [[vals[0][0]], 
                       [vals[1][0]]]
        valsResult2 = [[vals[0][1]], 
                       [vals[1][1]]]

        m1 = Matrix(vals)
        m2 = m1.SelectColumn(0)
        m3 = m1.SelectColumn(1)

        if m2.matrixVals != valsResult1:
            result = False 
        if m3.matrixVals != valsResult2:
            result = False

        return result
    def SelectRow(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult1 = [vals[0][0], 
                       vals[0][1]]
        valsResult2 = [vals[1][0], 
                       vals[1][1]]

        m1 = Matrix(vals)
        m2 = m1.SelectRow(0)
        m3 = m1.SelectRow(1)

        if m2 != valsResult1:
            result = False 
        if m3 != valsResult2:
            result = False

        return result
    def Sum(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = vals[0][0] + vals[1][0] + vals[0][1] + vals[1][1]

        m1 = Matrix(vals)
        m2 = m1.Sum()

        if m2 != valsResult:
            result = False 

        return result
    def MaxInVector(self): # Finished
        result = True
        vals = [randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)]
        valsResult = max(vals)

        m1 = Matrix(vals)
        m2 = m1.MaxInVector()[0]

        if m2 != valsResult:
            result = False 

        return result
    def Clear(self): # Finished
        result = True
        vals = [[randint(-10, 10) , randint(-10, 10)],
                [randint(-10, 10),  randint(-10, 10)]]
        valsResult = [[0, 0],
                      [0, 0]]

        m1 = Matrix(vals)
        m1.Clear()

        if m1.matrixVals != valsResult:
            result = False 

        return result
    def CombineVectorHorizontal(self): # Finished
        result = True

        vals1 = [randint(-10, 10) for i in range(2)]
        vals2 = [randint(-10, 10) for i in range(2)]
        valsResult = [[vals1[0], vals2[0]],
                      [vals1[1], vals2[1]]]

        v1 = Matrix(vals1)
        v2 = Matrix(vals2)
        v3 = Matrix.CombineVectorsHor([v1,v2])

        if v3.matrixVals != valsResult:
            result = False

        return result

# Method Exception Tests
    def MethodException(self):
        self.testResults["NotOfTypeVector"] = [self.NotOfTypeVector() for i in range(self.testCount)]
        self.testResults["VectorsNotOfSameLength"] = [self.VectorsNotOfSameLength() for i in range(self.testCount)]
        self.testResults["NoMatchingMultiplycase"] = [self.NoMatchingMultiplycase() for i in range(self.testCount)]
        self.testResults["NoMatchingAdditionCase"] = [self.NoMatchingAdditionCase() for i in range(self.testCount)]
        self.testResults["NoMatchingSubtractionCase"] = [self.NoMatchingSubtractionCase() for i in range(self.testCount)]
        self.testResults["NoMatchingPowerCase"] = [self.NoMatchingPowerCase() for i in range(self.testCount)]
        self.testResults["MismatchOrdersAdd"] = [self.MismatchOrdersAdd() for i in range(self.testCount)]
        self.testResults["MismatchOrdersSub"] = [self.MismatchOrdersSub() for i in range(self.testCount)]
        self.testResults["MismatchOrdersMul"] = [self.MismatchOrdersMul() for i in range(self.testCount)]
        self.testResults["SumOfMatrixReqNumericalVals"] = [self.SumOfMatrixReqNumericalVals() for i in range(self.testCount)]
        self.testResults["ColumnOutOfRange"] = [self.ColumnOutOfRange() for i in range(self.testCount)]
        self.testResults["ColumnMustBeInteger"] = [self.ColumnMustBeInteger() for i in range(self.testCount)]
        self.testResults["RowOutOfRange"] = [self.RowOutOfRange() for i in range(self.testCount)]
        self.testResults["RowMustBeInteger"] = [self.RowMustBeInteger() for i in range(self.testCount)]

    def NotOfTypeVector(self): # Finished
        try:
            m1 = Matrix((2,2))
            Matrix.CombineVectorsHor([m1, m1])
        except Exception as x:
            if x == MatExcepts.NotOfTypeVector: return True
            else: return False
    def VectorsNotOfSameLength(self): # Finished
        try:
            m1 = Matrix((2,1))
            m2 = Matrix((3,1))
            Matrix.CombineVectorsHor([m1, m2])
        except Exception as x:
            if x == MatExcepts.VectorsNotOfSameLength: return True
            else: return False
    def NoMatchingMultiplycase(self): # Finished
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 * m2
        except Exception as x:
            if x == MatExcepts.NoMatchingMultiplycase: return True
            else: return False
    def NoMatchingAdditionCase(self): # Finished
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 + m2
        except Exception as x:
            if x == MatExcepts.NoMatchingAdditionCase: return True
            else: return False
    def NoMatchingSubtractionCase(self): # Finished
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 - m2
        except Exception as x:
            if x == MatExcepts.NoMatchingSubtractionCase: return True
            else: return False
    def NoMatchingPowerCase(self): # Finished
        try:
            m1 = Matrix((2,1))
            m2 = randint(2,10) + 0.1
            m3 = m1 ** m2
        except Exception as x:
            if x == MatExcepts.NoMatchingPowerCase: return True
            else: return False
    def MismatchOrdersAdd(self): # Finished
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 + m2
        except Exception as x:
            if x == MatExcepts.MismatchOrders: return True
            else: return False
    def MismatchOrdersSub(self): # Finished
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 - m2
        except Exception as x:
            if x == MatExcepts.MismatchOrders: return True
            else: return False
    def MismatchOrdersMul(self): # Finished
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 * m2
        except Exception as x:
            if x == MatExcepts.MismatchOrders: return True
            else: return False
    def SumOfMatrixReqNumericalVals(self): # Finished
        try:
            M1 = Matrix([["1", "2"],
                        ["3", "4"]])
            m1Sum = M1.Sum() 
        except Exception as x:
            if x == MatExcepts.SumOfMatrixReqNumericalVals: return True
            else: return False
    def ColumnOutOfRange(self): # Finished
        try:
            m1 = Matrix((2,2))
            m2 = m1.SelectColumn(-1)
        except Exception as x:
            if x == MatExcepts.ColumnOutOfRange: return True
            else: return False
    def ColumnMustBeInteger(self): # Finished
        try:
            m1 = Matrix((3,3))
            m2 = m1.SelectColumn(1.5)
        except Exception as x:
            if x == MatExcepts.ColumnMustBeInteger: return True
            else: return False
    def RowOutOfRange(self): # Finished
        try:
            m1 = Matrix((2,2))
            m2 = m1.SelectRow(-1)
        except Exception as x:
            if x == MatExcepts.RowOutOfRange: return True
            else: return False
    def RowMustBeInteger(self): # Finished
        try:
            m1 = Matrix((3,3))
            m2 = m1.SelectRow(1.5)
        except Exception as x:
            if x == MatExcepts.RowMustBeInteger: return True
            else: return False

    def TestingResults(self):
        print("Unit Test Results:")

        for key in self.testResults:
            vals = self.testResults[key]
            count = sum(vals)

            print("{}/{} | {}".format(count, self.testCount, key))

MT = MatrixTest(0, 100000)
MT.RunAllTests()