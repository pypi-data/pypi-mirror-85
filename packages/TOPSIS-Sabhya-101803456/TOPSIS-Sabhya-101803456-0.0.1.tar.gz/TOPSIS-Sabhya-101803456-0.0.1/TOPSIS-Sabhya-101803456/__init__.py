import numpy as np
import pandas as pd
import math
import sys

try:
    if len(sys.argv)<5:
        raise Exception("Incorrect No of Parameters!")
    df = pd.read_csv(sys.argv[1])
    if (df.shape[1] < 3):
        raise Exception("Input file contains less than three columns !")
    y = df.iloc[:,1:5]
    x = y.values
    if(x.dtype == 'object'):
        raise Exception("Non Numeric Data Found!")
    weights_str=sys.argv[2]
    impacts_str = sys.argv[3]
    if weights_str.find(",") == -1 or impacts_str.find(",") == -1:
        raise Exception("Input not separated by commas")
    weights = np.array([int(x) for x in weights_str.split(",")])
    impacts = impacts_str.split(",")

    if not all(ele == '+' or ele == '-' for ele in impacts):
        raise Exception("Weights should be either + or -")

    if not (weights.size == len(impacts) == df.shape[1]-1):
        raise Exception("No of columns and No of input values dont match!")
    # Step 1 (vector normalization): cumsum() produces the
    # cumulative sum of the values in the array and can also
    # be used with a second argument to indicate the axis to use
    col_sums = np.array(np.cumsum(x**2, 0))
    norm_x = np.array([[round(x[i, j] / math.sqrt(col_sums[x.shape[0]- 1, j]), 3) for j in range(4)] for i in range(5)])

    # Step 2 (Multiply each evaluation by the associated weight):
    # wnx is the weighted normalized x matrix
    wnx = np.array([[round(weights[i] * norm_x[j, i], 3) for i in range(4)] for j in range(5)])

    # Step 3 (positive and negative ideal solution)
    #print(wnx)
    pis = np.array([np.amax(wnx[:, :1]), np.amax(wnx[:, 1:2]),np.amax(wnx[:, 2:3]), np.amax(wnx[:, 3:4])])
    #print(pis)
    nis = np.array([np.amin(wnx[:, :1]), np.amin(wnx[:, 1:2]),np.amin(wnx[:, 2:3]), np.amin(wnx[:, 3:4])])
    #print(nis)
    imp=[]
    for i in range(4):
        if(impacts[i] == '+'):
            imp.insert(i,pis[i])
        else:
            imp.insert(i,nis[i])

    #print(imp)

    # Step 4: determine the distance to the ideal
    # solution (dnis)
    b = np.array([[(wnx[j, i] - imp[i])**2 for i in range(4)] for j in range(5)])
    d = np.sum(b,axis=1)
    dnis = np.array([math.sqrt(d[i]) for i in range(5)])
    df.insert(5,'TOPSIS Score',dnis,True)
    # Step 5: calculate the relative closeness to the ideal
    # solution
    #final_solution = np.array([round(dnis[i] / (dpis[i] + dnis[i]),3) for i in range(5)])
    #print("Closeness coefficient = ", dnis)

    # Step 6: Sort the rank of the calculated cost
    temp = dnis.argsort()[::-1]
    ranks = np.empty_like(temp)
    ranks = np.arange(len(temp))[temp.argsort()]
    df.insert(6,'Rank',ranks+1,True)
    #print(df)
    df.to_csv(sys.argv[4])
except FileNotFoundError:
    print("File Not Found!")