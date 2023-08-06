import pandas as pd
import time
import math
import numpy as np
import sys as IN
import copy

arg = copy.deepcopy(IN.argv)

if len(IN.argv) != 5:
    print("Wrong number of parameters")
    IN.exit()

file = IN.argv[1]
result = IN.argv[4]
weights = IN.argv[2]
impacts = IN.argv[3]

if file.endswith(('.csv')):
    pass
else:
    print("File type not found")
    IN.exit()

try:
    weights = list(map(float, weights.split(',')))
    impacts = list(map(str, impacts.split(',')))
except:
    print('Weights or Impacts are not provided in proper format')
    IN.exit()

for each in impacts:
    if each not in ('+', '-'):
        print('Impacts are not provided in proper format')
        IN.exit()


if len(weights) != len(impacts):
    print("impacts and weights must have the same number of values")
    IN.exit()


input_data = pd.read_csv(file)
ncols = len(input_data.columns)


if ncols < 3:
    print("input file must have atleast 3 columns")
    IN.exit()


if(len(weights) != ncols-1 or len(impacts) != ncols - 1):
    print("The weights, impacts and the number of columns all should have the same number of values")
    IN.exit()

r_sos = []
ideal_best = []
ideal_worst = []
best_d = []
worst_d = []
max_score = []


def sos(input_data, r_sos):
    for i in range(1, len(input_data.columns)):
        col = input_data.iloc[:, i]
        sum = 0
        for j in col:
            sum = sum + j*j
        sum = np.sqrt(sum)
        r_sos.append(sum)
    return input_data


def norm_matr(input_data, r_sos):
    for i in range(1, len(input_data.columns)):
        col = input_data.iloc[:, i]
        for j in col:
            j = (j/r_sos[i-1])*weights[i-1]
    return input_data


def best(input_data, impacts, ideal_best):
    for i in range(1, len(input_data.columns)):
        if impacts[i-1] == '-':
            col = input_data.iloc[:, i]
            imin = col[0]
            for j in col:
                if j < imin:
                    imin = j
            ideal_best.append(imin)
        else:
            col = input_data.iloc[:, i]
            imax = col[0]
            for j in col:
                if j > imax:
                    imax = j
            ideal_best.append(imax)


def worst(input_data, impacts, ideal_worst):
    for i in range(1, len(input_data.columns)):
        if impacts[i-1] == '+':
            col = input_data.iloc[:, i]
            imin = col[0]
            for j in col:
                if j < imin:
                    imin = j
            ideal_worst.append(imin)
        else:
            col = input_data.iloc[:, i]
            imax = col[0]
            for j in col:
                if j > imax:
                    imax = j
            ideal_worst.append(imax)


def distances(input_data, best_d, worst_d, ideal_best, ideal_worst):
    for i in range(input_data.shape[0]):
        plus = 0
        minus = 0
        for j in range(1, len(input_data.columns)):
            plus += ((ideal_best[j-1]-input_data.iloc[i, j])
                     * (ideal_best[j-1]-input_data.iloc[i, j]))
            minus += ((ideal_worst[j-1]-input_data.iloc[i, j])
                      * (ideal_worst[j-1]-input_data.iloc[i, j]))
        best_d.append(np.sqrt(plus))
        worst_d.append(np.sqrt(minus))
    return input_data


input_data = sos(input_data, r_sos)
input_data = norm_matr(input_data, r_sos)
best(input_data, impacts, ideal_best)
worst(input_data, impacts, ideal_worst)
input_data = distances(input_data, best_d, worst_d, ideal_best, ideal_worst)


for i in range(input_data.shape[0]):
    max_score.append(worst_d[i]/(worst_d[i]+best_d[i]))

input_data['Topsis Score'] = max_score

in_data = pd.DataFrame(input_data)

in_data.sort_values(by=['Topsis Score'], ascending=False, inplace=True)

perf_score = dict()

rank = 1
for i in range(input_data.shape[0]):
    perf_score[in_data.iloc[i, 0]] = rank
    rank += 1

ranks = []
for i in range(input_data.shape[0]):
    ranks.append(perf_score[input_data.iloc[i, 0]])

input_data['Rank'] = ranks

input_data.to_csv(result, index=False, header=True)
