import sys,os.path, copy,time,math
import pandas as pd 
from os import path
import numpy as np
def check_source(source):
    if not (path.exists(source)): #check file exists or not
        print("No such file exists")
        exit(0)
    if not source.endswith('.csv'): #check format of input file
        print("Format is not supported")
        exit(0)
    file1 = pd.read_csv(source)
    col = file1.shape
    if not col[1]>=3: #check no. of columns
        print("Input file must contain three or more columns")
        exit(0)
    k =  0
    for i in file1.columns:
        k = k+1
        for j in file1.index:
            if k!=1:
                val =  isinstance(file1[i][j],int)
                val1 = isinstance(file1[i][j],float)
                if not val and not val1:
                    print(f'Value is not numeric in {k} column')
                    exit(0) 
    
def check_weight(source, w):
    file1 = pd.read_csv(source)
    col = file1.shape
    weight = []
    l = w.split(',')
    for i in l:
        k = 0
        for j in i:
            if not j.isnumeric():
                if k>=1 or j!='.':
                    print("Format of weight is not correct")
                    exit(0)
                else:
                    k = k+1
        weight.append(float(i))
    if len(weight) != (col[1]-1):
        print("No. of weights and no. of columns must be same")
        exit(0)
    return weight
        
def check_impact(source,im):
    file1 = pd.read_csv(source)
    col = file1.shape
    impact = im.split(',')
    for i in impact:
        if i not in {'+','-'} :
            print("Format of impact is not correct")
            exit(0)  
    if len(impact) != (col[1]-1) :
        print("No. of impacts and no. of columns must be same")
        exit(0)
    return impact

def normalized_matrix(source):
    check_source(source)
    df = pd.read_csv(source)
    col = list(df.columns)
    col.remove(col[0])
    for i in col:
        sum = 0
        for j in df.index:
            sum = sum+(df[i][j])*(df[i][j])
        sum = math.sqrt(sum)
        for j in df.index:
            df.at[j,i] = (df[i][j])/sum
    return df

def weight_normalized(source,we):
    df = normalized_matrix(source)
    w = check_weight(source,we)
    col = list(df.columns)
    col.remove(col[0])
    k = 0
    for i in col:
        for j in df.index:
            df.at[j,i] = w[k]*df[i][j]
        k = k+1
    return df

def ideal_best_worst(source,we,imp):
    df = weight_normalized(source,we)
    im = check_impact(source,imp)
    col = list(df.columns)
    col.remove(col[0])
    best = []
    worst = []
    k = 0
    for i in col:
        if im[k] == '+':
            best.append(max(df[i]))
            worst.append(min(df[i]))
        else:
            best.append(min(df[i]))
            worst.append(max(df[i]))
        k = k+1
    return (best,worst)

def euclidean_distance(source,we,imp):
    df = weight_normalized(source,we)
    col = list(df.columns)
    col.remove(col[0])
    best,worst = ideal_best_worst(source,we,imp)
    p1 = []
    p2 = []
    for i in df.index:
        sum1 = 0
        sum2 = 0
        k = 0
        for j in col:
            a = best[k]- df[j][i]
            b = worst[k] - df[j][i]
            sum1 = sum1 + a*a
            sum2 = sum2 + b*b
            k = k+1
        sum1 = math.sqrt(sum1)
        sum2 = math.sqrt(sum2)
        p1.append(sum1)
        p2.append(sum2)
    return (p1,p2)

def topsis_score(source,we,imp):
    p1,p2 = euclidean_distance(source,we,imp)
    d = pd.read_csv(source)
    n = len(p1)
    p = []
    for i in range(n):
        sum = p1[i]+p2[i]
        sum = p2[i]/sum
        p.append(sum)
    d['Topsis Score'] = p
    p = pd.Series(p)
    p = p.rank(ascending= False, method = 'min')
    d['Rank'] = p
    d['Rank'] = d['Rank'].astype('int')
    return d