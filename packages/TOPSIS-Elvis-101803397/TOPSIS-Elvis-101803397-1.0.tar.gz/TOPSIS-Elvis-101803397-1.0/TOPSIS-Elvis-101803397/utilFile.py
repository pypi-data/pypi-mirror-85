import os
import pandas as pd
import math

class TOPSIS:
    def read_file(self, InputfileName, OutputFileName):

        self.inputFileName = InputfileName
        self.outputFileName=OutputFileName
        intputfileName, inputfileExtension = os.path.splitext(InputfileName)
        outputfileName, outputfileExtension1 = os.path.splitext(OutputFileName)
        if intputfileName != '.csv' or outputfileName != '.csv':
            raise Exception("Incorrect File Format uploaded\nUpload .csv file")
        if (not os.path.exists(self.inputFileName)):
            raise Exception("File does not exist\nSpecify correct Path")
        self.dataFrame = pd.read_csv(self.inputFileName)
        if (self.dataFrame.isnull().values.any()):
            raise Exception("Missing values found in the input file\nPass the correct file")
        self.data = self.dataFrame.values
        self.data = self.data[:, 1:]
        if (self.data.shape[1] <= 2):
            raise Exception("Incorrect file format\nFile requires atleast three columns")
        return

    def read_weight_target(self, weight, target):
        self.weight = weight
        self.target = target

        if (len(self.weight) != len(self.target)):
            raise Exception("No of Weights and Targets mismatch")

        if (self.data.shape[1] != len(self.weight)):
            raise Exception("Input File Format and No. of Weights mismatch")

        for i in range(len(self.target)):
            if (self.target[i] != '+' and self.target[i] != '-'):
                raise Exception("TNon-specified characters in the Target\nIt can contain only '+' and '-' values")
        return
    def generate_score(self):

        rows = self.data.shape[0]
        cols = self.data.shape[1]
        under_squares = []
        for i in range(cols):
            under_squares.append(round(math.sqrt(sum(self.data[:, i] ** 2)), 2))
        for i in range(cols):
            for j in range(rows):
                self.data[j][i] = round(self.data[j][i] / under_squares[i], 2)

        for i in range(len(self.weight)):
            self.weight[i] = float(self.weight[i])

        for i in range(rows):
            for j in range(cols):
                self.data[i][j] = round(self.data[i][j] * self.weight[j], 2)

        ideal_best = []
        ideal_worst = []

        for i in range(cols):
            if (self.target[i] == '+'):
                ideal_best.append(max(self.data[:, i]))
                ideal_worst.append(min(self.data[:, i]))
            else:
                ideal_best.append(min(self.data[:, i]))
                ideal_worst.append(max(self.data[:, i]))
        euc_max = []
        euc_min = []

        for i in range(rows):
            temp = self.data[i, :]
            euc_max.append(round(math.sqrt(sum((temp - ideal_best) ** 2)), 2))
            euc_min.append(round(math.sqrt(sum((temp - ideal_worst) ** 2)), 2))

        self.topsis_score = []

        for i in range(rows):
            self.topsis_score.append(round((euc_min[i] / (euc_max[i] + euc_min[i])), 2))

        return self.topsis_score

    def findrank(self, array, index):
        temp = array[index]
        rank = 1
        for i in range(len(array)):
            if (array[i] > temp):
                rank = rank + 1
        return rank

    def generate_rank(self):
        self.rank = []

        for i in range(len(self.topsis_score)):
            self.rank.append(self.findrank(self.topsis_score, i))

        return self.rank

    def write_file(self):
        topsis = pd.DataFrame(self.topsis_score, columns=["Topsis Score"], index=None)
        ranks = pd.DataFrame(self.rank, columns=["Rank"], index=None)

        final_df = pd.concat([self.dataFrame, topsis, ranks], axis=1)

        final_df.to_csv(self.outputFileName, index=False)



