from cProfile import label
import matplotlib.pyplot as plt
import pickle

file = input()
#file2 = input()

dataPoints = []
with open("DataLogger\\" + file + ".data", "rb") as f:
    dataPoints = pickle.load(f)

#dataPoints2 = []
#with open("DataLogger\\" + file2 + ".data", "rb") as f:
#    dataPoints2 = pickle.load(f) 

averageLoss = [dataPoints[i][2] / 100 for i in range(len(dataPoints))]
#averageLoss2 = [dataPoints2[i][2] / 100 for i in range(len(dataPoints2))]
step = [dataPoints[i][3] for i in range(len(dataPoints))]
#step2 = [dataPoints2[i][3] for i in range(len(dataPoints2))]

#plt.plot(step, batch)
#plt.plot(step, maxbatch)
plt.plot(step, averageLoss)
#plt.plot(step2, averageLoss2, label="Neural Network")

plt.xlabel("Step Count")
plt.ylabel("Average Loss per Step")

plt.legend()
plt.show()