from heap import *
from datalogger import *
from deepqlearning import Deque
import random
from matrix import *

# 4.1

inputList = [[random.randint(-10,10), random.randint(-10,10)] for i in range(5)]
print("Unsorted List:")
for item in inputList:
    print(item)

dl = DataLogger("SortingTest", [int, int], False)

dl.LogDataPointBatch(inputList)

sortedList = dl.HeapSort(0)

print("Sorted List:")
for item in sortedList:
    print(item)

print() # 4.2

dl = DataLogger("AddPointTest", [int, int], False)
print("Before: ", dl.dataPoints)

dl.LogDataPoint([5, 2])

print("After: ", dl.dataPoints)

print() # 4.3

dl = DataLogger("Match Single Types", [int, float], False)

print("Matches Structure: ", dl.CheckMatchStructure([-3, 2.2]))

print() # 4.4

dl = DataLogger("Match Multi Typed", [bool, [float, int]], False)

print("Matches Structure: ", dl.CheckMatchStructure([False, 4.5]))
print("Matches Structure: ", dl.CheckMatchStructure([True, -9]))

print() # 4.5

dl = DataLogger("Match List Type", [bool, str], False)

print("Matches Structure: ", dl.CheckMatchStructure([True, ["Matt", "Isabel", "Tristan", "Chris"]]))

print() # 4.6

try:
    dl = DataLogger("Match Data Structure Error", [str, int], False)

    print("Matches Structure: ", dl.CheckMatchStructure(["Steve Preston", True]))
except Exception as x:
    print(x)

print() # 4.7

inputList = [[random.randint(-10,10), random.randint(-10,10)] for i in range(5)]
print("Random List:")
for item in inputList:
    print(item)

dl = DataLogger("Select List", [int, int], False)

dl.LogDataPointBatch(inputList)

sortedList = dl.Select(0, [1,2,3,5,7])

print("Selected List:")
for item in sortedList:
    print(item)

print() # 4.8

inputList = [[random.randint(-10,10), random.randint(-10,10)] for i in range(5)]
print("Saved List:")
for item in inputList:
    print(item)

dl = DataLogger("Save-Load Test", [int, int], False)

dl.LogDataPointBatch(inputList)

dl.SaveDataPoints()

print() # 4.9

dl = DataLogger("Save-Load Test", [int, int], True)

print("Loaded List:")
for item in dl.dataPoints:
    print(item)

print() # 3.8

deque = Deque(10)
deque.PushFront(3)
print("Added 3:", deque.queue)
deque.PushFront(-5)
print("Added -1:", deque.queue)
deque.PushFront(9)
print("Added 9:", deque.queue)

print() # 3.9

deque = Deque(4)
deque.PushFront(3)
deque.PushFront(-5)
deque.PushFront(9)
deque.PushFront(4)
deque.PushFront(-4)

print("First:", deque.First())
print("Last:", deque.Last())
print("Queue:", deque.queue)

print() # 3.10

deque = Deque(4)
deque.PushFront(3)
deque.PushFront(-5)
deque.PushFront(9)
deque.PushFront(4)
deque.PushFront(-4)

print("Sample 1:", deque.Sample(2))
print("Sample 2:", deque.Sample(2))
print(deque.queue)

print() # 3.11

# Experience Replay

print() # 3.12

# Activation Outputs

print() # 3.13

# Activation Derivatives

print() # 2.1

matrix = Matrix((3, 4))
print(matrix)

print() # 2.2

values = [[3, 4],
          [1, 2]]
matrix = Matrix(values)
print(matrix)

print() # 2.3

values = [1, 2, 3, 4]
matrix = Matrix(values)
print(matrix)

print() # 2.4

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)
print(matrix)

print() # 2.5

matrix = Matrix((2, 2), random=True)
print(matrix)

print() # 2.6

matrix = Matrix((3, 3), identity=True)
print(matrix)

print() # 2.7

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)
values2 = [[3, 4],
          [1, 2]]
matrix2 = Matrix(values2)

result = matrix + matrix2
print(result)

print() # 2.8

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)
values2 = [[3, 4],
          [1, 2]]
matrix2 = Matrix(values2)

result = matrix - matrix2
print(result)

print() # 2.9

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)
values2 = [[3, 4],
          [1, 2]]
matrix2 = Matrix(values2)

result = matrix * matrix2
print(result)

print() # 2.10

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)

result = matrix * 3 
print(result)

print() # 2.11

values = [1, 2, 3, 4]
vector = Matrix(values)

values = [4, 3, 2, 1]
vector2 = Matrix(values)

result = vector * vector2
print(result)

print() # 2.12

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)

result = matrix ** 5
print(result)

print() # 2.13

values = [[4, 3],
          [2, 1]]
matrix = Matrix(values)

result = matrix.Transpose()
print(result)

print() # 2.14

values = [[4, 3, 6],
          [2, 1, 5]]
matrix = Matrix(values)

result = matrix.SelectColumn(1)
print(result)

print() # 2.15

values = [[4, 3, 6],
          [2, 1, 5]]
matrix = Matrix(values)

result = matrix.SelectRow(0)
print(result)

print() # 2.16

values = [4, 3, 6, 1, 2, 5]
vector = Matrix(values)

result = vector.MaxInVector()
print(result)

print() # 2.17

values = [[4, 3, 6],
          [2, 1, 5]]
matrix = Matrix(values)

matrix.Clear()
print(matrix)

print() # 2.18

values = [1, 2, 3, 4]
vector = Matrix(values)

values = [4, 3, 2, 1]
vector2 = Matrix(values)

vectorList = [vector, vector2]

result = Matrix.CombineVectorsHor(vectorList)
print(result)

print() # 2.19

values = [[4, 3, 6],
          [2, 1, 5]]
matrix = Matrix(values)

result = matrix.Sum()
print(result)