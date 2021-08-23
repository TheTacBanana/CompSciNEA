import math, random
class Matrix():
    def __init__ (self, Values, cols = 0, identity = False):
        if type(Values) == list: # Predefined Values
            self.matrixArr = Values
            
        elif identity == True: # Identity Matrix
            if Values != cols:
                raise Exception("Cant create Identity Matrix of different orders")
            else:
                self.matrixArr = [[0 for i in range(cols)] for j in range(Values)]
                for y in range(0, Values):
                    self.matrixArr[y][y] = 1

        elif Values > 0 and cols > 0: # Blank Matrix of size x by y
            self.matrixArr = [[0 for i in range(cols)] for j in range(Values)]

        else: # Error Creating Matrix
            raise Exception("Error Creating Matrix")

    def Val(self):
        return self.matrixArr

    def Dimensions(self):
        return [len(self.matrixArr), len(self.matrixArr[0])] # Rows - Columns

    def ScalarMultiply(self, multiplier):
        for y in range(0, len(self.matrixArr)):
            for x in range(0, len(self.matrixArr[0])):
                self.matrixArr[y][x] = self.matrixArr[y][x] * multiplier

    def SubMatrixList(self, rowList, colList):
        newMat = Matrix(self.Dimensions()[0] - len(rowList),self.Dimensions()[1] - len(colList))
        xoffset = 0
        yoffset = 0
        yRowList = []

        for y in range(0, self.Dimensions()[0]):
            for x in range(0, self.Dimensions()[1]):
                if x in colList and y in rowList:
                    xoffset += 1
                    yoffset += 1
                    continue
                elif x in colList:
                    xoffset += 1
                    continue
                elif y in rowList and y not in yRowList:
                    yoffset += 1
                    yRowList.append(y)
                    continue
                else:
                    newMat.matrixArr[y - yoffset][x - xoffset] = self.matrixArr[y][x]
            xoffset = 0
        return newMat


    def SubMatrixRange(self, y1, y2, x1, x2):
        subMat = Matrix(y2 - y1 + 1, x2 - x1 + 1)
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                subMat.matrixArr[y][x] = self.matrixArr[y][x]
        return subMat

    def RandomVal(self):
        self.matrixArr = [[random.randint(1, 100) for i in range(self.Dimensions()[1])] for j in range(self.Dimensions()[0])]

    def ConvertToVector(self):
        return Vector(self.matrixArr)

    @staticmethod
    def Determinant(m):
        dims = m.Dimensions()
        if dims[1] <= 2:
            det = (m.matrixArr[0][0] * m.matrixArr[1][1]) - (m.matrixArr[0][1] * m.matrixArr[1][0])
            return (det)
        elif dims[1] != 2:
            det = 0
            subtract = False
            tempMat = m.SubMatrixList([0],[])
            for i in range(0, dims[1]):
                subMat = None
                subMat = m.SubMatrixList([0],[i])
                if subtract == False:
                    det += m.matrixArr[0][i] * Matrix.Determinant(subMat)
                    subtract = True
                elif subtract == True:
                    det -= m.matrixArr[0][i] * Matrix.Determinant(subMat)
                    subtract = False
            return det

    def det(m):
        top_length = len(m[0])
        height = top_length - 1
        submats = []

        for i in range(0, top_length):
            submat = [[] for i in range(height)]
            for j in range(0, top_length):
                if i != j:
                    for k in range(height):
                        submat[k].append(m[k+1][j])
            submats.append(submat)
        return submats

    # Static Methods
    @staticmethod
    def MatrixAddSubtract(m1, m2, subtract = False): # Dont know how else i would make this more efficient lol
        m1Dims = m1.Dimensions()
        m2Dims = m2.Dimensions()
        if m1Dims[0] != m2Dims[0]:
            raise Exception("Matrices Row Order does not match")
        elif m1Dims[1] != m2Dims[1]:
            raise Exception("Matrices Column Order does not match")
        elif type(m1) != type():
            raise Exception("Types do not match, Convert Vector to Matrix or vice verse")
        else:
            newMat = Matrix(m1Dims[0], m1Dims[1])
            for y in range(0, m1Dims[0]):
                for x in range(0, m1Dims[1]):
                    if subtract:
                        newMat.matrixArr[y][x] = m1.Val()[y][x] - m2.Val()[y][x]
                    else:
                        newMat.matrixArr[y][x] = m1.Val()[y][x] + m2.Val()[y][x]
            return newMat

    @staticmethod
    def MatrixMultiply(m1, m2): # Not that efficient, needs optimisation
        m1Dims = m1.Dimensions()
        m2Dims = m2.Dimensions()
        if m1Dims[1] != m2Dims[0]:
            raise Exception("Matrices Multiplication Error")
        else:
            if(type(m2) == Vector):
                newMat = Matrix(m1Dims[0], m2Dims[1])
            else:
                newMat = Matrix(m1Dims[0], m2Dims[1])
            for row in range(0, m1Dims[1]):
                subRow = m1.Val()[row][0:m1Dims[1]]
                for col in range(0, m2Dims[1]):
                    subCol = []
                    for i in range(0, m1Dims[0]):
                        print(i)
                        subCol.append(m2.Val()[i][col])
                    total = 0
                    for x in range(0, len(subRow)):
                        total += subRow[x] * subCol[x]
                    newMat.matrixArr[row][col] = total
            return newMat

class Vector(Matrix):
    def __init__(self, val):
        if type(val) == list:
            if len(val[0]) != 1:
                raise Exception("Invalid Vector, use Matrix Instead")
            else:
                self.matrixArr = val
        else:
            self.matrixArr = [[0 for i in range(1)] for j in range(val)]

    def ConvertToMatrix(self):
        return Matrix(self.matrixArr)

    @staticmethod
    def DotProduct(v1,v2):
        if type(v1) != Vector or type(v2) != Vector:
            raise Exception("Wront Types:{},{} passed into Dot Product".format(type(v1),type(v2)))
        else:
            total = 0
            for i in range(v1.Dimensions()[0]):
                total += v1.Val()[i][0] * v2.Val()[i][0]
            return total

class GraphStuff():
    # Constants
    pi = 3.141592653589793
    e = 2.718281828459045

    @staticmethod   # Squishy function
    def Sigmoid(x): 
        return 1/(1 + (GraphStuff().e) ** (-x))

    #Sin Tan Cos
    @staticmethod
    def Sin(x):
        return math.sin(x)
    @staticmethod
    def Cos(x):
        return math.cos(x)
    @staticmethod
    def Tan(x):
        return math.tan(x)