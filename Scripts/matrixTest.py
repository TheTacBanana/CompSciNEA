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
        print(self.MultiplicationMatrix())
        print(self.Power())
        print(self.Transpose())
        print(self.SelectColumn())
        print(self.SelectRow())
        print(self.CombineVectorHorizontal())

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
    def Sum(self):
        pass
    def MaxInVector(self):
        pass
    def Clear(self):
        pass
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
        print(self.NotOfTypeVector())
        print(self.VectorsNotOfSameLength())

    def NotOfTypeVector(self):
        try:
            m1 = Matrix((2,2))
            Matrix.CombineVectorsHor([m1, m1])
        except Exception as x:
            if x == MatExcepts.NotOfTypeVector: return True
            else: return False

    def VectorsNotOfSameLength(self):
        try:
            m1 = Matrix((2,1))
            m2 = Matrix((3,1))
            Matrix.CombineVectorsHor([m1, m2])
        except Exception as x:
            if x == MatExcepts.VectorsNotOfSameLength: return True
            else: return False

    def NoMatchingMultiplycase(self):
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 * m2
        except Exception as x:
            if x == MatExcepts.NoMatchingMultiplycase: return True
            else: return False

    def NoMatchingAdditionCase(self):
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 + m2
        except Exception as x:
            if x == MatExcepts.NoMatchingAdditionCase: return True
            else: return False

    def NoMatchingSubtractionCase(self):
        try:
            m1 = Matrix((2,1))
            m2 = "Test Data"
            m3 = m1 - m2
        except Exception as x:
            if x == MatExcepts.NoMatchingSubtractionCase: return True
            else: return False

    def NoMatchingPowerCase(self):
        try:
            m1 = Matrix((2,1))
            m2 = randint(2,10) + 0.1
            m3 = m1 ** m2
        except Exception as x:
            if x == MatExcepts.NoMatchingPowerCase: return True
            else: return False
    
    def MismatchOrdersAdd(self):
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 + m2
        except Exception as x:
            if x == MatExcepts.MismatchOrdersAdd: return True
            else: return False

    def MismatchOrdersSub(self):
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 - m2
        except Exception as x:
            if x == MatExcepts.MismatchOrdersAdd: return True
            else: return False

    def MismatchOrdersMul(self):
        try:
            m1 = Matrix((2,2))
            m2 = Matrix((3,3))
            m3 = m1 * m2
        except Exception as x:
            if x == MatExcepts.MismatchOrdersMul: return True
            else: return False

    def SumOfMatrixReqNumericalVals(self):
        pass

    def ColumnOutOfRange(self):
        pass

    def ColumnMustBeInteger(self):
        pass

    def RowOutOfRange(self):
        pass

    def RowMustBeInteger(self):
        pass

    def TestingResults(self):
        pass

MT = MatrixTest(0)
MT.RunAllTests()