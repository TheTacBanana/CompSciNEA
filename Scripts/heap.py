import math

# A Binary tree with the heap property, such that for every element, both children are <= to the parent
class Heap:
    def __init__(self, elements, indexIn): # Creates a new heap from a list of elements, and assigns an index for which to sort by
        self.elements = elements
        self.index = indexIn

        self.Heapify()

    def AddElement(self, element): # Adds Singular element to Heap
        self.elements.append(element)
        self.SiftUp(len(self.elements) - 1)

    def SiftUp(self, elementIndex): # Sifts a singular element up the heap if possible
        newElementIndex = elementIndex
        isHeap = False

        while not isHeap: # Repeat until is a heap again
            parentIndex = math.floor((newElementIndex - 1) / 2)

            if parentIndex == 0 and newElementIndex == 0: # Base Case
                isHeap = True

            elif self.elements[newElementIndex][self.index] >= self.elements[parentIndex][self.index]: # Swaps elements which dont conform to heap property
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

        while ((2 * rootIndex) + 1) <= end: # Repeat until the next root index is outside the dimensions of the heap
            childIndex = (rootIndex * 2) + 1

            if childIndex + 1 <= end and self.elements[childIndex][self.index] < self.elements[childIndex + 1][self.index]: # Checks which child is larger
                childIndex += 1

            if self.elements[rootIndex][self.index] < self.elements[childIndex][self.index]: # Swapping elements which dont conform to Heap rules
                tempSwap = self.elements[childIndex]
                self.elements[childIndex] = self.elements[rootIndex]
                self.elements[rootIndex] = tempSwap

                rootIndex = childIndex
            else:
                break

    def RemoveTop(self): # Pops top element off of Heap and returns it, heapifies the heap once removed
        tempSwap = self.elements[-1]
        self.elements[-1] = self.elements[0] # Swaps First and Last elements
        self.elements[0] = tempSwap

        returnElement = self.elements[-1] # Stores and deletes the final element
        self.elements = self.elements[:-1]

        self.Heapify() # Creates Heap again

        return returnElement # Returns Top element

    def Peek(self): # Returns root/top element
        return self.elements[0]

    def Length(self): # Returns size of heap
        return len(self.elements)

    def Heapify(self): # Returns values to a heap form, where all children of parents are less than or equal too
        for i in range(math.floor((len(self.elements) - 1) / 2), -1, -1):
            self.SiftDown(i)