import matplotlib.pyplot as plt
import pickle
from os import listdir
from os.path import isfile, join
from typing import DefaultDict

def LoadFileList(dir): # Locating files in directory and returning them as a dictionary
    directoryList = listdir(dir)
    validFiles = [f for f in directoryList if isfile(join(dir, f))]

    fileDict = DefaultDict(str)

    for i in range(len(validFiles)):
        fileDict[i] = validFiles[i]

    return fileDict

def PickChoice(fileDict): # Pick choice from file dictionary
    print("List of Data Files:")
    for file in fileDict:
        print(str(file) + " : " + fileDict[file])

    inp = eval(input())
    if isinstance(inp, int):
        return fileDict[inp]
    else:
        raise Exception("Not a valid input")

def LoadPoints(file): # Load Data Points from file
    dataPoints = []
    with open("DataLogger\\" + file, "rb") as f:
        dataPoints = pickle.load(f)
    return dataPoints

# Logic
fileDictionary = LoadFileList("DataLogger\\")
file = PickChoice(fileDictionary)
dataPoints = LoadPoints(file)

print("Plot: ")
inp = eval(input())

plottedData = [dataPoints[i][inp] / 100 for i in range(len(dataPoints))]
step = [dataPoints[i][-1] for i in range(len(dataPoints))]

# Setup Plot
plt.plot(step, plottedData)
plt.xlabel("Step Count")
plt.ylabel("Average Loss per Step")

plt.show()