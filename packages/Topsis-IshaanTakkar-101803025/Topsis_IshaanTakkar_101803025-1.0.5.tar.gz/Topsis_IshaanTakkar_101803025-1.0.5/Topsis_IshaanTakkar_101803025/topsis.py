# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:56:40 2020

@author: ishaan takkar
"""
import pandas as pd
import numpy as np
import math
import sys
import os


def main():
    if len(sys.argv) != 5:
     print("Error!! wrong number of parameters")
     print("Pass four parameters")
     print("usages:-python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName> ")
     print("e.g:- python topsismain.py data.csv '1,1,1,1' '+,+,-,+' finaloutput.csv")
     sys.exit(0)
     try:
      d=open(sys.argv[1])
     except:
        print ("Error !! something goes wrong ")
        print ("Wrong file or file path ")
        print ("Incorrect parameters may be given")
     x=os.path.splitext(sys.argv[1])
     if( x !='.csv' ):
      raise Exception('file extension should be csv')

    else:
        df= pd.read_csv(sys.argv[1])
        tdf= pd.read_csv(sys.argv[1])
        nCol = len(tdf.columns)

        if nCol < 3:
            print("error!! Something goes wrong")
            print("File should have atleast 3 parameters")
            sys.exit(0)
            
    print(" No error found\n\n Applying Topsis Algorithm...\n")
    
    w=sys.argv[2].split(',')
    for i in range(len(w)):
        if w[i]=="'1" or w[i]=="1'":
            w[i]='1'
    weights=[]
    for j in range(len(w)): 
        weights.append(int(w[j]))
    impact=sys.argv[3].split(',')
    
    for i in range(len(impact)):
        if impact[i]=="'+" or impact[i]=="+'":
            impact[i]='+'
        if impact[i]=="'-" or impact[i]=="-'":
            impact[i]='-'
    for i in range(len(impact)):
        if impact[i]!="+" and impact[i]!="-":
            print("Error!")
            print("Impact is either + or -")
            sys.exit(0)
    num=[]
    for i in range(nCol):
        if df.iloc[:,i:i+1].dtypes[0]=='float64':
            num.append(df.iloc[:,i:i+1].columns[0])
    if len(weights)!=len(num) and len(impact)!=len(num):
        print("Error!")
        sys.exit(0)
    print(" Generating Score and Rank...\n")
    non_num=[]
    for i in df.columns:
        if i not in num:
            non_num.append(i)
    sqrt_column_sum=[]
    for i in df.columns:
        if i in num:
            sqrt_column_sum.append(round(math.sqrt(df[i].pow(2).sum(axis=0)),2))
    j=0
    for i in df.columns:
        if i in num:
            df[i]=round(df[i].div(sqrt_column_sum[j]),2)
            j=j+1
    j=0
    for i in df.columns:
        if i in num:
            df[i]=round((df[i]*weights[j]),2)
            j=j+1
    V_pos=[]
    j=0
    for i in num:
        if impact[j]=='+':
            V_pos.append(df[i].max())
        else:
            V_pos.append(df[i].min())
        j=j+1
    V_neg=[]
    j=0
    for i in num:
        if impact[j]=='+':
            V_neg.append(df[i].min())
        else:
            V_neg.append(df[i].max())
        j=j+1
    fd=df.drop(non_num,axis=1)
    arr=fd.to_numpy()
    r=len(arr)
    c=len(arr[0])
    S_pos=[]
    s=0
    for i in range(r):
        for j in range(c):
            s=s+(arr[i][j]-V_pos[j])**(2)
        S_pos.append(round(math.sqrt(s),2))
        s=0
    S_neg=[]
    s=0
    for i in range(r):
        for j in range(c):
            s=s+(arr[i][j]-V_neg[j])**(2)
        S_neg.append(round(math.sqrt(s),2))
        s=0
    per=[]
    for i in range(r):
        per.append(round(S_neg[i]/(S_neg[i]+S_pos[i]),2))
    p=pd.DataFrame(per,index=None,columns=['per'])
    fd['TOPSIS SCORE']=per
    fd['Rank'] = fd['TOPSIS SCORE'].rank(ascending=0)
    if os.path.isfile(sys.argv[4]):
        print("File already exists!!")
        sys.exit(0)
    print(" Writing Result to CSV...\n")
    fd.to_csv(sys.argv[4])
    print(" Successfully Terminated")


if __name__ == "__main__":
    main()

