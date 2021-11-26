from matrix import *
from random import randint, seed

class MatrixTest():
    def __init__(self, seed):
        seed(seed)

        self.ConstructorTests = {"CreateVectorFrom1DList": False,
                                 "CreateMatrixFrom2DList": False,
                                 "CreateMatrixFromTuple": False,
                                 "CreateIdentityMatrix": False}

        self.ConstructorExceptions = {"NoMatchingInitCase": False,
                                      "UnableToCreateIdentityMat": False}

        self.MethodUnitTests = {"Addition": False,
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
        self.MethodUnitTests()
        self.MethodExceptions()

        self.TestingResults()

    def ConstructorTest(self):
        # CreateVectorFrom1DList
        v1 = Matrix([randint(-10, 10) for i in range(randint(3, 10))])

        if v1.order[0] == len(v1) and v1.order[1] == 1:
            self.ConstructorTests["CreateVectorFrom1DList"] = True
        else:
            self.ConstructorTests["CreateVectorFrom1DList"] = False

        # CreateMatrixFrom2DList
        m1 = Matrix([[3 , -4],
                     [-1,  5]])

        if m1.order[0] == 2 and m1.order[1] == 2:
            self.ConstructorTest["CreateMatrixFrom2DList"] = True
        else:
            self.ConstructorTest["CreateMatrixFrom2DList"] = False

        # CreateMatrixFromTuple
        order = (randint(-10, 10), randint(-10, 10))
        m2 = Matrix(order)
        if m2.order == order:
            self.ConstructorTest["CreateMatrixFrom2DList"] = True

    def ConstructorExceptionsTest(self):
        pass

    def MethodUnitTests(self):
        pass

    def MethodExceptions(self):
        pass

    def TestingResults(self):
        pass