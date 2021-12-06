import pickle, random
from heap import *
from time import time

# Data Collector Class for logging information for analysis
class DataCollector():
    def __init__(self, name, dataStructure, load=True): # Constructor Method
        self.name = name

        self.dataStructure = dataStructure

        if load: # Loads Data if available but else create blank
            self.dataPoints = DataCollector.LoadDataPoints(name)
        else:
            self.dataPoints = []

    def LogDataPointBatch(self, dataPoints): # Logs a Batch of Data Points
        for i in range(len(dataPoints)):
            self.LogDataPoint(dataPoints[i])

    def LogDataPoint(self, dataPoint): # Logs Data Point to Data Point list
        if self.CheckMatchStructure(dataPoint):
            self.dataPoints.append(dataPoint)


    def CheckMatchStructure(self, dataPoint): # Checks the given Data Point is in the correct Form
        if len(dataPoint) != len(self.dataStructure): # Throws error if lengths dont match
            raise Exception("Structure of Data Point does not match Collector Specified Structure")

        for i in range(len(dataPoint)):
            t1 = type(dataPoint[i]) # Type 1 
            t2 = self.dataStructure[i] # Type 2

            if t1 == list and type(t2) != list: # Checks if list is all of same type
                flag = False

                for x in range(len(dataPoint[i])):
                    if type(dataPoint[i][x]) != t2:
                        flag = True
                if not flag:
                    continue

            elif t1 == list and type(t2) == list: # Checks list against list
                if len(dataPoint[i]) == len(t2):
                    flag = False
                    for x in range(len(dataPoint[i])):
                        if type(dataPoint[i][x]) != t2[x]:
                            flag = True

                    if not flag:
                        continue

            elif type(t2) == list: # Checks Multiple types against t1
                flag = False

                for x in range(len(t2)):
                    if t1 == t2[x]:
                        flag = True
                if flag:
                    continue

            else:                # Checks Singular type against t1
                if t1 == t2:
                    continue

            raise Exception(("Type: {} != Data Structure Type: {} \n {}").format(t1, t2, self.dataStructure))
        return True

    def HeapSort(self, parameterIndex): # O(n*log n) sorting algorithm utilising a Heap Data structure, Sorts the data points by the specified parameter
        # 1000 Items -> 0.13
        # 10000 Items -> 12.1
        # 100000 Items -> 1646 or 27.4 minutes

        if type(self.dataStructure[parameterIndex]) == list: # Throw error if data structure element is List
            raise Exception("Cannot sort by structure: {}".format(type(self.dataStructure[parameterIndex])))

        elif self.dataStructure[parameterIndex] == bool: # Throw error if data structure element is Bool
            raise Exception("Cannot sort by structure: {}".format(self.dataStructure[parameterIndex]))

        sortedList = []

        heap = Heap(self.dataPoints, parameterIndex) # Creates a new heap

        while heap.Length() - 1 >= 0:
            sortedList.append(heap.RemoveTop()) # Loops popping and appending greatest element from Heap

        return sortedList

    def Select(self, searchIndex, searchContents): # Select a specified element with contents from data points
        returnedList = []

        for i in range(len(self.dataPoints)):
            if self.dataPoints[i][searchIndex] in searchContents:
                returnedList.append(self.dataPoints[i])

        return returnedList

    # Using Pickle to Save/Load
    @staticmethod
    def LoadDataPoints(file): # Returns stored dataPoints
        with open("DataLogger\\" + file + ".data", "rb") as f:
            temp = pickle.load(f)
        return temp

    def SaveDataPoints(self): # Saves dataPoints to a file
        with open("DataLogger\\" + self.name + ".data", "wb") as f:
            pickle.dump(self.dataPoints, f)