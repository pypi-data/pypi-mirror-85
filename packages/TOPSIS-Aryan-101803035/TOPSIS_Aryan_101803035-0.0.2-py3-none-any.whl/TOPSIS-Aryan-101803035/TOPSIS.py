# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:23:35 2020

@author: aryan
"""


import pandas as pd
import numpy as np
import sys
import math as m
import string
import copy

if len(sys.argv) != 5:
    print('Incorrect number of parameters.')
    sys.exit()

filename = sys.argv[1]

try:
    dataframe = pd.read_csv(filename)
except FileNotFoundError:
    print("Wrong file or file path")
    exit()

dataframe2 = copy.deepcopy(dataframe)

if len(dataframe2.columns) < 3:
    print("Input file must contain three or more columns.")
    exit()

weights = sys.argv[2]
weights = list(map(float, weights.split(',')))


impacts = sys.argv[3]
impacts = list(map(str, impacts.split(',')))

try:
    data = dataframe2.iloc[:, 1:].values.astype(float)
except ValueError:
    print("Only numeric values allowed.")
    exit()

(rows, cols) = data.shape

t = sum(weights)

if len(weights) != cols:
    print("No of weights is unequal.")
    exit()
if len(impacts) != cols:
    print("No of impacts is unequal.")
    exit()

for i in impacts:
    if i!='+' and i!='-':
        print("Impacts should be '+' or '-' only.")
        exit()

for i in string.punctuation:
    if i != ',':
        if i in weights:
            print("Weights must be separated by Comma(',').")
            exit()
        if i != '+' and i != '-' and i in impacts:
            print("Impacts must be separated by Comma(',').")
            exit()


for i in range(cols):
    weights[i] /= t

a = [0.0] * cols

for i in range(0, rows):
    for j in range(0, cols):
        a[j] = a[j] + (data[i][j] * data[i][j])

for j in range(cols):
    a[j] = m.sqrt(a[j])

for i in range(rows):
    for j in range(cols):
        data[i][j] /= a[j]
        data[i][j] *= weights[j]


idp = np.amax(data, axis=0)  # MAX IN VERTICAL COLUMN
idn = np.amin(data, axis=0)  # MIN IN EACH COLUMN
for i in range(len(impacts)):
    if impacts[i] == '-':  
        temp = idp[i]
        idp[i] = idn[i]
        idn[i] = temp

pos_dist = list()
neg_dist = list()

for i in range(rows):
    t = 0
    for j in range(cols):
        t += pow((data[i][j] - idp[j]), 2)

    pos_dist.append(float(pow(t, 0.5)))

for i in range(rows):
    t = 0
    for j in range(cols):
        t += pow((data[i][j] - idn[j]), 2)

    neg_dist.append(float(pow(t, 0.5)))

performance_score = dict()

for i in range(rows):
    performance_score[i + 1] = neg_dist[i] / (neg_dist[i] + pos_dist[i])

a = list(performance_score.values())
b = sorted(list(performance_score.values()), reverse=True)

rank = dict()

for i in range(len(a)):
    rank[(b.index(a[i]) + 1)] = a[i]
    b[b.index(a[i])] = -b[b.index(a[i])]

row = list(i + 1 for i in range(len(b)))
a = list(rank.values())
rk = list(rank.keys())

dataframe2['Topsis Score'] = a
dataframe2['Rank'] = rk
output = pd.DataFrame(dataframe2)

result_name = sys.argv[4]
output.to_csv(result_name, index=False)