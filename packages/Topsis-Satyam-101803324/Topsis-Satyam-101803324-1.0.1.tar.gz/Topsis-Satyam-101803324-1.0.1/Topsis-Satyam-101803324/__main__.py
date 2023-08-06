import pandas as pd
import time
import math
import numpy as np
import sys as adm
import copy

arg = copy.deepcopy(adm.argv)

if len(adm.argv) != 5:
    print("Wrong number of parameters. Total of 5 should be there.")
    adm.exit()

inputFile = adm.argv[1]
weights = adm.argv[2]
impacts = adm.argv[3]
resultFileName = adm.argv[4]

if inputFile.endswith(('.csv')):
    pass
else:
    print("File not found. Should be a .csv")
    adm.exit()

try:
    weights = list(map(float, weights.split(',')))
    impacts = list(map(str, impacts.split(',')))
except:
    print('Weights or Impacts are not provided in proper format')
    adm.exit()

for each in impacts:
    if each not in ('+', '-'):
        print('Impacts are not provided in proper format')
        adm.exit()

if len(weights) != len(impacts):
    print("impacts and weights must have the same number of arguments")
    adm.exit()
    

input_df = pd.read_csv(inputFile)
totalCol = len(input_df.columns)


if totalCol < 3:
    print("input file must have atleast 3 columns")
    adm.exit()


if(len(weights) != totalCol-1 or len(impacts) != totalCol - 1):
    print("The weights, impacts and the number of columns all should have the equal number of values")
    adm.exit()

rSos = []
idealBest = []
idealWorst = []
bestD = []
worstD = []
max_score = []


def sos(input_df, rSos):
    for i in range(1, len(input_df.columns)):
        col = input_df.iloc[:, i]
        sum = 0
        for j in col:
            sum = sum + j*j
        sum = np.sqrt(sum)
        rSos.append(sum)
    return input_df


def normOfMat(input_df, rSos):
    for i in range(1, len(input_df.columns)):
        col = input_df.iloc[:, i]
        for j in col:
            j = (j/rSos[i-1])*weights[i-1]
    return input_df


def findBest(input_df, impacts, idealBest):
    for i in range(1, len(input_df.columns)):
        if impacts[i-1] == '-':
            col = input_df.iloc[:, i]
            imin = col[0]
            for j in col:
                if j < imin:
                    imin = j
            idealBest.append(imin)
        else:
            col = input_df.iloc[:, i]
            imax = col[0]
            for j in col:
                if j > imax:
                    imax = j
            idealBest.append(imax)


def findWorst(input_df, impacts, idealWorst):
    for i in range(1, len(input_df.columns)):
        if impacts[i-1] == '+':
            col = input_df.iloc[:, i]
            imin = col[0]
            for j in col:
                if j < imin:
                    imin = j
            idealWorst.append(imin)
        else:
            col = input_df.iloc[:, i]
            imax = col[0]
            for j in col:
                if j > imax:
                    imax = j
            idealWorst.append(imax)


def distances(input_df, bestD, worstD, idealBest, idealWorst):
    for i in range(input_df.shape[0]):
        plus = 0
        minus = 0
        for j in range(1, len(input_df.columns)):
            plus += ((idealBest[j-1]-input_df.iloc[i, j])
                     * (idealBest[j-1]-input_df.iloc[i, j]))
            minus += ((idealWorst[j-1]-input_df.iloc[i, j])
                      * (idealWorst[j-1]-input_df.iloc[i, j]))
        bestD.append(np.sqrt(plus))
        worstD.append(np.sqrt(minus))
    return input_df


input_df = sos(input_df, rSos)
input_df = normOfMat(input_df, rSos)
findBest(input_df, impacts, idealBest)
findWorst(input_df, impacts, idealWorst)
input_df = distances(input_df, bestD, worstD, idealBest, idealWorst)


for i in range(input_df.shape[0]):
    max_score.append(worstD[i]/(worstD[i]+bestD[i]))

input_df['Topsis Score'] = max_score

in_df = pd.DataFrame(input_df)

in_df.sort_values(by=['Topsis Score'], ascending=False, inplace=True)

perf_score = dict()

rank = 1
for i in range(input_df.shape[0]):
    perf_score[in_df.iloc[i, 0]] = rank
    rank += 1

ranks = []
for i in range(input_df.shape[0]):
    ranks.append(perf_score[input_df.iloc[i, 0]])

input_df['Rank'] = ranks

input_df.to_csv(resultFileName, index=False, header=True)
