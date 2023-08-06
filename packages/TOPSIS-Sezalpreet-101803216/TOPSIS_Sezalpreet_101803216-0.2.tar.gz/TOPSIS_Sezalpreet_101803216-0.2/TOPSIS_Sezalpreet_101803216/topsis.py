import pandas as pd
import sys
import os
from os import path
import numpy as np
import math as m
import csv

if len(sys.argv) != 5:
    print("Wrong number of arguments")
    exit(0)

if path.exists(sys.argv[1]) == False:
    print("Input File doesn't exist")
    exit(0)

filename = sys.argv[1]
data = pd.read_csv(filename)
columns = list(data.columns)

df = data.iloc[ :,1:].values.astype(float)
row = data.shape[0]
col = data.shape[1]
if col < 3:
    print("Invalid number of columns")

weights = sys.argv[2]
impacts = sys.argv[3]

weights = list(map(float ,weights.split(',')))
impacts = list(map(str ,impacts.split(',')))

if len(weights) != col:
    print("Insufficient weights")
    exit(0)
if len(impacts) != col:
    print("Insufficient impacts")
    exit(0)
for i in range(len(impacts)):           # checking for impacts(+ or -)
    if impacts[i] != '+' or impacts[i] != '-':
        exit(0)

s = sum(weights)
for i in range(col):
    weights[i] = weights[i]/s

arr = [0]*(col)

for i in range (0,row):
    for j in range(0,col):
        arr[j] = arr[j] + (df[i][j]*df[i][j])

for i in range(col):
    arr[i] = m.sqrt(arr[i])

for i in range(row):
    for j in range(col):
        df[i][j]/=arr[j]
        df[i][j]*=weights[j]

ideal_best = np.amax(df , axis=0)
ideal_worst = np.amin(df , axis=0)

for i in range(len(impacts)):
    if impacts[i]=="-":
        temp = ideal_best[i]
        ideal_best[i] = ideal_worst[i]
        ideal_worst[i] = temp

best = list()
worst = list()

for i in range(row):
    s = 0
    for j in range(col):
        s += pow((data[i][j]-ideal_best[j]), 2)

    best.append(float(pow(s, 0.5)))


for i in range(row):
    s=0
    for j in range(col):
        s += pow((data[i][j]-ideal_worst[j]), 2)

    worst.append(float(pow(s, 0.5)))

tops_score = dict()
for i in range(row):
    tops_score[i+1] = worst[i]/(best[i]+worst[i])

a = list(tops_score.values())
b = sorted(list(tops_score.values()), reverse=True)

rank = dict()

for i in range(len(a)):
    rank[(b.index(a[i]) + 1)] = a[i]
    b[b.index(a[i])] = -b[b.index(a[i])]

a = list(rank.values())
R = list(rank.keys())

final = dict()

d = df.iloc[:].values
r = d.shape[0]
c = d.shape[1]
for i in range(r):
    k = list()
    for j in range(c):
        k.append(d[i][j])
    k.append(a[i])
    k.append(R[i])
    final[i] = k

columns.append("Topsis Score")
columns.append("Rank")

f = open(sys.argv[4], 'w')
csvwriter = csv.writer(f)  # creating a csv writer object
csvwriter.writerow(columns)  # writing the fields
for l in range(len(final)):
    csvwriter.writerow(final[l])  # writing the data rows
f.close()




