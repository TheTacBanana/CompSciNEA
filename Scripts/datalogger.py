import pickle

# Data Collector Class for logging information for analysis
class DataCollector():
    def __init__(self, name, dataStructure, load=True): # Constructor Method
        self.name = name

        self.dataStructure = dataStructure

        if load:
            self.dataPoints = DataColletor.LoadDataPoints(name)
        else:
            self.dataPoints = []

    def LogDataPointBatch(self, dataPoints): # Logs a Batch of Data Points
        for i in range(len(dataPoints)):
            self.LogDataPoint(dataPoints[i])

    def LogDataPoint(self, dataPoint): # Logs Data Point to Data Point list
        if self.CheckMatchStructure(dataPoint):
            self.dataPoints.append(dataPoint)

    def CheckMatchStructure(self, dataPoint): # Checks the given Data Point is in the correct Form
        if len(dataPoint) != len(self.dataStructure):
            raise Exception("Structure of Data Point does not match Collector Specified Structure")

        for i in range(len(dataPoint)):
            t1 = type(dataPoint[i])
            t2 = self.dataStructure[i]

            if type(t2) == list: # Checks Multiple types against t1
                flag = False

                for i in range(len(t2)):
                    if t1 == t2[i]:
                        flag = True
                if flag:
                    continue

            else:                # Checks Singular type against t1
                if t1 == t2:
                    continue

            raise Exception(("Type: {} != Data Structure Type: {} \n {}").format(t1, t2, self.dataStructure))
        return True

    # Using Pickle to Save/Load
    @staticmethod
    def LoadDataPoints(file): # Returns stored Neural Network data
        with open("DataLogger\\" + self.name + ".data", "rb") as f:
            temp = pickle.load(f)
        return temp

    def SaveDataPoints(self, file): # Saves Neural Network Data
        with open("DataLogger\\" + self.name + ".data", "wb") as f:
            pickle.dump(self.dataPoints)