import sys
import pandas as pd
import numpy as np
import copy
import os

if len(sys.argv) != 5:
    print("ERROR. INCORRECT NUMBER OF ARGUMENTS")
    print("Atleast 4 parameters required")
    print("usage: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    print("example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv")
    exit(0)

NumberOfArguments = len(sys.argv)
filename = sys.argv[1]
resultFile = sys.argv[NumberOfArguments - 1]

inputFile = pd.read_csv(sys.argv[1])
originalInput = copy.deepcopy(inputFile)
attributes = inputFile.columns

if (len(attributes) < 3):
    print("Error: Input File should contain atleast 3 columns.")
    exit(0)

w = sys.argv[2]
imp = sys.argv[3]

commasCountInWeight = w.count(',')
commasCountInImpact = imp.count(',')

if commasCountInWeight != len(attributes) - 2 or commasCountInImpact != len(attributes) - 2:
    print("Weight and Impact values must be comma separated.")
    exit(0)

weights = []
impacts = []

for i in range(0, len(imp)):
    if imp[i] == ',':
        continue;
    impacts.append(imp[i])

n = ''
for i in range(0, len(w)):
    if w[i] == ',':
        weights.append(float(n))
        n = ''
        continue
    n = n + w[i]

weights.append(float(n))

if len(weights) != len(impacts) or len(weights) != len(attributes) - 1 or len(impacts) != len(attributes) - 1:
    print("Error: Length of weights array, impacts array and number of columns from 2nd one to last should be equal.")
    exit(0)

for i in impacts:
    if i == '+' or i == '-':
        continue;
    print("Error: Impacts value can be either '+' or '-'.")
    exit(0)

sum_weights = sum(weights)
weights = [i / sum_weights for i in weights]

try:
    totalParameters = len(weights)

    FirstAttribute = attributes[0]
    inputFile.drop(attributes[0], axis="columns", inplace=True)

    attributes = inputFile.columns

    j = 0;
    summationSqrt = 0


    def fun(x):
        return (x / summationSqrt) * weights[j];


    for i in range(0, len(attributes)):
        temp = inputFile[attributes[i]]
        summation = 0
        for k in temp:
            summation += k * k;
        summationSqrt = np.sqrt(summation)
        dfList = inputFile[attributes[i]].apply(fun)
        inputFile[attributes[i]] = dfList
        j += 1

    idealValues = []
    maxValues = inputFile.max()
    minValues = inputFile.min()

    for i in range(0, totalParameters):
        if impacts[i] == '+':
            idealValues.append([maxValues[i], minValues[i]])
        else:
            idealValues.append([minValues[i], maxValues[i]])

    Spositive = []
    Snegative = []

    arrayList = []
    sh = inputFile.shape
    totalElements = sh[0]
    for i in range(0, totalParameters):
        temp = inputFile[attributes[i]]
        arrayList.append(temp)

    for i in range(0, totalElements):
        forPositive = 0;
        forNegative = 0;
        for j in range(0, totalParameters):
            tempForPos = abs(arrayList[j][i] - idealValues[j][0])
            tempForNeg = abs(arrayList[j][i] - idealValues[j][1])
            forPositive += tempForPos * tempForPos;
            forNegative += tempForNeg * tempForNeg;
        Spositive.append(np.sqrt(forPositive))
        Snegative.append(np.sqrt(forNegative))

    performanceScore = []

    for i in range(0, totalElements):
        temp = Spositive[i] + Snegative[i]
        pi = Snegative[i] / temp
        performanceScore.append(pi)

    originalInput["Topsis Score"] = performanceScore
    originalInput['Rank'] = originalInput['Topsis Score'].rank(ascending=0)
    originalInput.set_index(FirstAttribute, inplace=True)
    originalInput.to_csv(resultFile, mode="w", header="False")
except:
    print(" Error!! Something went wrong ")
    print("- Incorrect parameter given")
    print("- File not found")
    print('- Enter only numeric values')
