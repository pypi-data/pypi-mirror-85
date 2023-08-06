import pandas as pd
import numpy as np
import math as m
import copy
import sys
import os.path
from os import path

if len(sys.argv)!=5:
    print("Incorrect number of command line parameters")
    exit()

fileName=sys.argv[1]
try:
    fp=open(fileName)        # Open the file in reading mode
    fp.close()
except:
    print ("Error !! %s file Not Found"%(fileName))
    exit()

  
rd = pd.read_csv(sys.argv[1])
rd = rd.drop(['Model'],axis=1)
df = pd.read_csv(sys.argv[1])
df = df.drop(['Model'],axis=1)
r = rd.shape[0]
c = rd.shape[1]
temp = rd.applymap(np.isreal)

# Checking non numeric entry
for i in range(r):
    for j in range(c):
        if temp.iloc[i][j]=='False':
            print("Non numeric entry found")
            exit()

weights = list(map(int, sys.argv[2].split(',')))

impact = list(map(str, sys.argv[3].split(',')))

if len(rd.columns) + len(weights) + len(impact) !=12:
    print("Number of weights, number of impacts and number of columns must be same")
    exit()
for i in impact:
    if i !='+' and i!='-':
        print("Impact can be either + or -")
        exit()

cols = list(rd.columns)



l=[]


# Normalising
for i in range(c):
    sum=0
    for j in range(r):
        sum+=(rd.iloc[j,i]*rd.iloc[j,i])
    l.append(m.sqrt(sum))

for i in range(c):
    for j in range(r):
        rd.iloc[j,i] = rd.iloc[j,i]/l[i]


# multiplying by weights
for i in range(c):
    for j in range(r):
        rd.iloc[j,i] = rd.iloc[j,i]*int(weights[i])

best=[]
worst=[]
# print(rd)

for i in range(c):
    if impact[i] == '+':
        best.append(rd.iloc[:,i].max())
        worst.append(rd.iloc[:,i].min())
    else:    
        best.append(rd.iloc[:,i].min())
        worst.append(rd.iloc[:,i].max())
# print(best)        
b_col=[]
w_col=[]
 
for i in range(r):
    sum_b=0
    sum_w=0
    for j in range(c):
        
        sum_b+=(rd.iloc[i,j]-best[j])**2
        sum_w+=(rd.iloc[i,j]-worst[j])**2
    b_col.append(m.sqrt(sum_b))
    w_col.append(m.sqrt(sum_w))

top_score=[]

for i in range(r):
    top_score.append(w_col[i]/(w_col[i]+b_col[i]))

rank = [0,0,0,0,0]
ori = copy.deepcopy(top_score)
top_score.sort(reverse=True)

c=1
for i in top_score:
    rank[ori.index(i)]= c
    c+=1


df['Topsis Score'] = ori
df['Rank'] = rank

df.to_csv(sys.argv[4],index=False) 



