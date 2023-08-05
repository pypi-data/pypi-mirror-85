import math
import pandas as pd
import numpy as np
import csv
import sys
import time
from scipy.stats import rankdata
import argparse
from csv import reader
from collections import Counter


def top(file,impacts,weights):
    datas=data=pd.read_csv(file)
    weights= list(weights.split(","))
    impacts= list(impacts.split(","))
    positive=[]
    negative=[]
    for i in range(0, len(weights)):
        weights[i] = int(weights[i])
    datas=data.iloc[:,1:].values
    rows= len(datas)
    cols=list(data.columns)
    square = []
    positive =[]
    negative = []
    for i in range(0, len(cols)-1):
        sum=0
        for j in range(0,rows):
            sum = sum + (datas[j,i]*datas[j,i])
        temp= math.sqrt(sum)    
        square.append(temp)
    
    for i in range(0, len(cols)-1):
        for j in range(0,rows):
            datas[j,i]= datas[j,i]/square[i]
            datas[j,i]= datas[j,i]*weights[i]
            
    for i in range(0, len(cols)-1):
        min = 100000000
        max = -100000000
        for j in range(0,rows):
            if min > datas[j,i]:
                min= datas[j,i]
            if max < datas[j,i]:
                max = datas[j,i]
        if impacts[i] == '+':
            positive.append(max)
            negative.append(min)
        if impacts[i] == '-':
            positive.append(min)
            negative.append(max)

    spositive = []
    snegative = []
    performance = []
    
    for i in range(0,rows):    
        sum=0
        sum1 = 0
        for j in range(0, len(cols)-1):
            sum = sum + (datas[i,j]-positive[j])*(datas[i,j]-positive[j])
            sum1 = sum1 + (datas[i,j]-negative[j])*(datas[i,j]-negative[j])
        sum = math.sqrt(sum)
        sum1 = math.sqrt(sum1)
        spositive.append(sum)
        snegative.append(sum1)
    for i in range(0,len(spositive)):
        performance.append(snegative[i]/(spositive[i]+snegative[i]))

    rank = len(performance) - rankdata(performance, method = 'min').astype(int) + 1
    datas = np.column_stack((datas,performance))
    datas = np.column_stack((datas,rank))
    column_name=np.array(data.columns)
    name=np.array(['Topsis Score','Rank'])
    x=np.concatenate((column_name,name))
    c=np.array(data.iloc[:,0])
    temp = datas
    temp = np.column_stack((c, temp))
    temp = np.vstack ((x, temp) )
    DF = pd.DataFrame(temp)
    DF.to_csv("C:\\Users\\hp\\Desktop\\result.csv",header=False,index=False)
    print("done")
top("C:\\Users\\hp\\Desktop\\data.csv","+,+,-,+","1,1,1,1")
