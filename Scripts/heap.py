import math

class Heap:
    def __init__(self, rootElements, indexIn):
        self.elements = rootElements
        self.index = indexIn

        self.Heapify()

    def AddElement(self, element): # Adds Singular element to Heap
        self.elements.append(element)
        self.SiftUp(len(self.elements) - 1)

    def SiftUp(self, elementIndex): # Sifts a singular element up the heap if possible
        newElementIndex = elementIndex
        isHeap = False

        while not isHeap:
            parentIndex = math.floor((newElementIndex - 1) / 2)

            if parentIndex == 0 and newElementIndex == 0:
                isHeap = True

            elif self.elements[newElementIndex][self.index] >= self.elements[parentIndex][self.index]:
                tempSwap = self.elements[parentIndex]
                self.elements[parentIndex] = self.elements[newElementIndex]
                self.elements[newElementIndex] = tempSwap

                newElementIndex = parentIndex
            else:
                isHeap = True

    def SiftDown(self, elementIndex): # Sifts a singular element down the heap if possible
        rootIndex = elementIndex
        isHeap = False

        end = len(self.elements) - 1

        while ((2 * rootIndex) + 1) <= end:
            childIndex = (rootIndex * 2) + 1

            if childIndex + 1 <= end and self.elements[childIndex][self.index] < self.elements[childIndex + 1][self.index]:
                childIndex += 1

            if self.elements[rootIndex][self.index] < self.elements[childIndex][self.index]:
                tempSwap = self.elements[childIndex]
                self.elements[childIndex] = self.elements[rootIndex]
                self.elements[rootIndex] = tempSwap

                rootIndex = childIndex
            else:
                break

    def RemoveTop(self): # Pops top element off of Heap and returns it, heapifies the heap once removed
        tempSwap = self.elements[-1]
        self.elements[-1] = self.elements[0]
        self.elements[0] = tempSwap

        returnElement = self.elements[-1]
        self.elements = self.elements[:-1]

        self.Heapify()

        return returnElement

    def Peek(self): # Returns root/top element
        return self.elements[0]

    def Length(self):
        return len(self.elements)

    def Heapify(self): # Returns values to a heap form, where all children of parents are less than or equal too
        for i in range(len(self.elements), -1, -1):
            self.SiftDown(i)