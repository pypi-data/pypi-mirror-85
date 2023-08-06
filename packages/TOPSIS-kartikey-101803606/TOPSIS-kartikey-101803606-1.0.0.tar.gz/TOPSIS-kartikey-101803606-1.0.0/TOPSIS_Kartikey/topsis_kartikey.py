# Kartikey Nigam 101803606

def topsis(inputFile, weights, impacts, outputFile):
    import math as m
    import pandas as pd
    import numpy as np
    import sys
    import os
    if os.path.exists(inputFile) == False:
        print("No such file exists")
        sys.exit(0)
    extensionCheck = [inputFile, outputFile]
    for val in extensionCheck:
        temp = val.split('.')
        if temp[1] != "csv":
            print("Only .csv files allowed")
            sys.exit(0)


    weights = weights.split(',')
    impacts = impacts.split(',')
    weights = list(map(float, weights))
    impacts = list(map(str, impacts))
    dataset = pd.read_csv(inputFile)


    if dataset.shape[1] < 3:
        print("Number of columns should be greater than or equal to 3")
        sys.exit(0)

    def isNumeric(x):
        try:
            x = float(x)
            if (isinstance(x, int) == True or isinstance(x, float) == True):
                return True
        except:
            print("Not a numeric value in columns 2nd or further")
            sys.exit(0)
        return False

    for i in range(1, dataset.shape[1]):
        for j in range(dataset.shape[0]):
            if(isNumeric(dataset.iloc[j,i])) == False:
                print(dataset.iloc[j,i])
                print("All the values in 2nd column and further should be numeric")
                sys.exit(0)

    for x in impacts:
        if not(x == '+' or x == '-'):
            print("Impacts must be either + or -")
            sys.exit(0)

    data = dataset.iloc[ :,1:].values.astype(float)
    (r,c) = data.shape
    s = sum(weights)


    if not(len(weights) == len(impacts) == c):
        print("Insufficient Values")
        sys.exit(0)


    for i in range(c):
        weights[i] /= s

    a = [0]*(c)

    for i in range(0,r):
        for j in range(0,c):
            a[j]=a[j]+(data[i][j]*data[i][j])

    for j in range(c):
        a[j]=m.sqrt(a[j])

    for i in range(r):
        for j in range(c):
            data[i][j]/=a[j]
            data[i][j]*=weights[j]

    idealPositive = np.amax(data,axis=0)
    idealNegative = np.amin(data,axis=0)
    for i in range(len(impacts)):
        if(impacts[i] == '-'):
            temp = idealPositive[i]
            idealPositive[i] = idealNegative[i]
            idealNegative[i] = temp

    distPos = list()
    distNeg = list()

    for i in range(r):
        s=0
        for j in range(c):
            s += pow((data[i][j] - idealPositive[j]), 2)

        distPos.append(float(pow(s,0.5)))


    for i in range(r):
        s=0
        for j in range(c):
            s += pow((data[i][j]-idealNegative[j]), 2)

        distNeg.append(float(pow(s,0.5)))

    performanceScore = dict()

    for i in range(r):
        performanceScore[i+1] = distNeg[i]/(distNeg[i] + distPos[i])

    a = list(performanceScore.values())
    b = sorted(list(performanceScore.values()) , reverse=True)

    rank = dict()

    for i in range(len(a)):
        rank[(b.index(a[i]) + 1)] = a[i]
        b[b.index(a[i])] =-b[b.index(a[i])]

    row = list(i+1 for i in range(len(b)))
    a = list(rank.values())
    rr = list(rank.keys())
    out = {'Model':row,'Performance Score' : a , 'Rank':rr}
    output = pd.DataFrame(out)
    output.to_csv(outputFile, index = False)
    print(output)
