import matplotlib.pyplot as plt
import pickle
from os import listdir
from os.path import isfile, join
from typing import DefaultDict

def LoadFileList(dir): # Locating files in directory and returning them as a dictionary
    validFiles = [f for f in listdir(dir) if isfile(join(dir, f))]

    fileDict = DefaultDict(str)

    for i in range(len(validFiles)):
        fileDict[i] = validFiles[i]

    return fileDict

def PickChoice(fileDict): # Pick choice from file dictionary
    print("List of Data Files:")
    for file in fileDict:
        print(str(file) + " : " + fileDict[file])

    inp = eval(input())
    return fileDict[inp]

def LoadPoints(file): # Load Data Points from file
    dataPoints = []
    with open("DataLogger\\" + file, "rb") as f:
        dataPoints = pickle.load(f)
    return dataPoints

fileDictionary = LoadFileList("DataLogger\\")
file = PickChoice(fileDictionary)
dataPoints = LoadPoints(file)

averageLoss = [dataPoints[i][2] / 100 for i in range(len(dataPoints)) if i % 5 == 0]
step = [dataPoints[i][3] for i in range(len(dataPoints)) if i % 5 == 0]

plt.plot(step, averageLoss)

plt.xlabel("Step Count")
plt.ylabel("Average Loss per Step")

plt.show()