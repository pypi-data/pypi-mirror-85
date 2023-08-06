#Created by Kaustubh Bhatt | TIET | Patiala

def topsis(input_file, w, impacts, output_file):
    import math as m
    import pandas as pd
    import numpy as np
    import sys
    import os
    if os.path.exists(input_file) == False:
        print("The requested file Does Not Exist")
        sys.exit(0)
    
    in_check = input_file.split('.')
    if in_check[1] != "csv":
        print("input file must be csv.")
        sys.exit(0)
    out_check = output_file.split('.')
    if out_check[1] != "csv":
        print("output file must be csv")
        sys.exit(0)    


    w = w.split(',')
    impacts = impacts.split(',')
    w = list(map(float, w))
    impacts = list(map(str, impacts))
    dataset = pd.read_csv(input_file)


    if dataset.shape[1] < 3:
        print("Number of columns must be greater than 2")
        sys.exit(0)

    def checkNumeric(val):
        try:
            val = float(val)
            if (isinstance(val, int) == True or isinstance(val, float) == True):
                return True
        except:
            print("The value should be a numeric value")
            sys.exit(0)
        return False

    for i in range(1, dataset.shape[1]):
        for j in range(dataset.shape[0]):
            if(checkNumeric(dataset.iloc[j,i])) == False:
                print(dataset.iloc[j,i])
                print("The value must be numeric.")
                sys.exit(0)

    for val in impacts:
        if not(val == '+' or val == '-'):
            print("value of impact must be + or -")
            sys.exit(0)

    data = dataset.iloc[ :,1:].values.astype(float)
    (row,column) = data.shape
    s = sum(w)

    if not(len(w) == len(impacts) == column):
        print("Insufficient Values")
        sys.exit(0)

    for i in range(column):
        w[i] /= s

    a = [0]*(column)

    for i in range(0,row):
        for j in range(0,column):
            a[j]=a[j]+(data[i][j]*data[i][j])

    for j in range(column):
        a[j]=m.sqrt(a[j])

    for i in range(row):
        for j in range(column):
            data[i][j]/=a[j]
            data[i][j]*=w[j]

    idealPositive = np.amax(data,axis=0)
    idealNegative = np.amin(data,axis=0)
    for i in range(len(impacts)):
        if(impacts[i] == '-'):
            temp = idealPositive[i]
            idealPositive[i] = idealNegative[i]
            idealNegative[i] = temp

    distPos = list()
    distNeg = list()

    for i in range(row):
        s=0
        for j in range(column):
            s += pow((data[i][j] - idealPositive[j]), 2)

        distPos.append(float(pow(s,0.5)))

    for i in range(row):
        s=0
        for j in range(column):
            s += pow((data[i][j]-idealNegative[j]), 2)

        distNeg.append(float(pow(s,0.5)))
    performanceScore = dict()

    for i in range(row):
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
    output.to_csv(output_file, index = False)
    print(output)