# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 20:24:42 2020

@author: Snehal
"""

import pandas as pd 
from os import path

def check_source(file):
    if not (path.exists(file)): #check file exists or not
        print("No such file exists")
        exit(0)
    if not file.endswith('.csv'): #check format of input file
        print("Format not supported")
        exit(0)
    file1=pd.read_csv(file)
    num=file1.shape
    if not num[1]>=3: #check no. of columns
        print("Input file must contain three or more columns")
        exit(0)
    k=0
    for i in file1.columns:
        k = k+1
        for j in file1.index:
            if k!=1:
                val=isinstance(file1[i][j],int)
                val1=isinstance(file1[i][j],float)
                if not val and not val1:
                    print("All columns except first must contain numeric values only")
                    exit(0) 
def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True
    
def check_weight(file, w):
    file1=pd.read_csv(file)
    col=file1.shape
    v=w.split(',')
    for i in v:
        if not is_number(i):
            print("Format of weight is not correct")
            exit(0)
    if len(v)!= (col[1]-1):
        print("No. of weights and no. of columns must be same")
        exit(0)
    return v
        
def check_impact(file,im):
    file1=pd.read_csv(file)
    col=file1.shape
    v=im.split(',')
    for i in v:
        if i not in ('+','-'):
            print("Format of impact is not correct")
            exit(0)
    if len(v)!=(col[1]-1):
        print("No. of weights and no. of columns must be same")
        exit(0)
    return v

def square_and_divide(file):
    check_source(file)
    df=pd.read_csv(file)
    col=list(df.columns)
    col.remove(col[0])
    c=0
    s=0
    for j in col:
        for i in df.index:
            c=c+(df.iloc[i][j]**2)
        #print(c)
        s=c**0.5
        for i in df.index:
            df.at[i,j]=df.iloc[i][j]/s
    return df

def multiply_weightage(file,weight):
    df=square_and_divide(file)
    w=check_weight(file,weight)
    col=list(df.columns)
    col.remove(col[0])
    k = 0
    for k,j in zip(w,col):
        for i in df.index:
            df.at[i,j]=df.iloc[i][j]*int(k)
    return df

def best_worst_value(file,weight,impact):
    df=square_and_divide(file)
    weights=check_weight(file,weight)
    col=list(df.columns)
    col.remove(col[0])
    k = 0
    for k,j in zip(weights,col):
        for i in df.index:
            df.at[i,j]=df.iloc[i][j]*int(k)
    impacts=check_impact(file,impact)
    best = []
    worst = []
    for m,j in zip(impacts,col):
        if m=='+':
            best.append(max(df[j]))
            worst.append(min(df[j]))
        else:
            best.append(min(df[j]))
            worst.append(max(df[j]))
    return (best,worst)

def topsis_score(file,weight,impact):
    d=pd.read_csv(file)
    df=multiply_weightage(file,weight)
    col = list(df.columns)
    col.remove(col[0])
    best,worst=best_worst_value(file,weight,impact)
    performance_scores=[]
    for i in df.index:
        b=0
        w=0
        for ind,j in enumerate(col):
            b=b+((df[j][i]-best[ind])**2)
            w=w+((df[j][i]-worst[ind])**2)
        s1=b**0.5
        s2=w**0.5
        score=s2/(s1+s2)
        performance_scores.append(score)
    d['Topsis Score']=performance_scores
    return d

def rank(file,weight,impact):
    d=topsis_score(file,weight,impact)
    p=list(d['Topsis Score'])
    p=pd.Series(p)
    p = p.rank(ascending= False, method = 'min')
    d['Rank']=p
    d['Rank']=d['Rank'].astype('int')
    return d
