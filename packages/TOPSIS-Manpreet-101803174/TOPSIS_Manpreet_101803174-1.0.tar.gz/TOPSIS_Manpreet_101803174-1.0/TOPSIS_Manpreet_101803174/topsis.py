import sys
import pandas as pd
import numpy as np
import copy
import os

def topsis():
    NumberOfArguments = len(sys.argv)

    filename = sys.argv[1]
    resultFile = sys.argv[NumberOfArguments-1]
      
    inputFile = pd.read_csv(sys.argv[1])
    originalInput = copy.deepcopy(inputFile)
    attributes = inputFile.columns


    w = sys.argv[2]
    imp = sys.argv[3]

    commasCountInWeight = w.count(',')
    commasCountInImpact = imp.count(',')


    weights = []
    impacts = []

    for i in range(0,len(imp)):
        if imp[i] == ',':
            continue;
        impacts.append(imp[i])

    n = ''
    for i in range(0,len(w)):
        if w[i] == ',':
            weights.append(float(n))
            n = ''
            continue
        n = n + w[i]

    weights.append(float(n))

    sum_weights = sum(weights)
    weights = [i/sum_weights for i in weights]


    totalParameters = len(weights)

    FirstAttribute = attributes[0]
    inputFile.drop(attributes[0],axis="columns",inplace=True)

    attributes = inputFile.columns

    j = 0;
    summationSqrt = 0
    def fun(x):
        return (x/summationSqrt)*weights[j];

    for i in range(0,len(attributes)):
        temp = inputFile[attributes[i]]
        summation = 0
        for k in temp:
            summation += k*k;
        summationSqrt = np.sqrt(summation)
        dfList = inputFile[attributes[i]].apply(fun)
        inputFile[attributes[i]] = dfList
        j += 1

    idealValues = []  

    maxValues = inputFile.max()
    minValues = inputFile.min()

    for i in range(0,totalParameters):
        if impacts[i] == '+':
            idealValues.append([maxValues[i],minValues[i]])
        else:
            idealValues.append([minValues[i],maxValues[i]])

    Spositive = []
    Snegative = []

    arrayList = []
    sh = inputFile.shape
    totalElements = sh[0]
    for i in range(0,totalParameters):
        temp = inputFile[attributes[i]]
        arrayList.append(temp)

    for i in range(0,totalElements):
        forPositive = 0;
        forNegative = 0;
        for j in range(0,totalParameters):
            tempForPos = abs(arrayList[j][i]-idealValues[j][0])
            tempForNeg = abs(arrayList[j][i]-idealValues[j][1])
            forPositive += tempForPos*tempForPos;
            forNegative += tempForNeg*tempForNeg;
        Spositive.append(np.sqrt(forPositive))
        Snegative.append(np.sqrt(forNegative))
        
    performanceScore = []

    for i in range(0,totalElements):
        temp = Spositive[i] + Snegative[i]
        pi = Snegative[i]/temp
        performanceScore.append(pi)

    dictionary = {}
    dictionary2 = {}
    for i in range(0,totalElements):
        dictionary.update({performanceScore[i]:i})

    j = 1
    for i in sorted(dictionary,reverse=True):
        dictionary2.update({i:j})
        j += 1

    def function(x):
        return dictionary2[x]

    originalInput["Topsis Score"] = performanceScore
    temp = originalInput["Topsis Score"].apply(function)
    originalInput["Rank"] = temp;
    originalInput.set_index(FirstAttribute,inplace=True)
    originalInput.to_csv(resultFile,mode="w",header="False")


if __name__ == "__main__":
    topsis()
