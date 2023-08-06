import pandas as pd
import numpy as np
import math
import sys
import os
def get_weight(a):
    w=a.split(',')
    for i in range(len(w)):
        if w[i]=="'1" or w[i]=="1'":
            w[i]='1'
    weights=[]
    for j in range(len(w)): 
        weights.append(int(w[j]))
    return weights
def get_impact(a):
    impact=a.split(',')
    for i in range(len(impact)):
        if impact[i]=="'+" or impact[i]=="+'":
            impact[i]='+'
        if impact[i]=="'-" or impact[i]=="-'":
            impact[i]='-'
    return impact
def num_col(df,n_cols):
    num=[]
    for i in range(n_cols):
        if df.iloc[:,i:i+1].dtypes[0]=='float64':
            num.append(df.iloc[:,i:i+1].columns[0])
    return num
def non_num_col(df,num):
    non_num=[]
    for i in df.columns:
        if i not in num:
            non_num.append(i)
    return non_num
def weight_normalised(df,num,weights):
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
    return df
def V_positive(df,num,impact):
    V_pos=[]
    j=0
    for i in num:
        if impact[j]=='+':
            V_pos.append(df[i].max())
        else:
            V_pos.append(df[i].min())
        j=j+1
    return V_pos
def V_negative(df,num,impact):
    V_neg=[]
    j=0
    for i in num:
        if impact[j]=='+':
            V_neg.append(df[i].min())
        else:
            V_neg.append(df[i].max())
        j=j+1
    return V_neg
def S_positive(arr,r,c,V_pos):
    S_pos=[]
    s=0
    for i in range(r):
        for j in range(c):
            s=s+(arr[i][j]-V_pos[j])**(2)
        S_pos.append(round(math.sqrt(s),2))
        s=0
    return S_pos
def S_negative(arr,r,c,V_neg):
    S_neg=[]
    s=0
    for i in range(r):
        for j in range(c):
            s=s+(arr[i][j]-V_neg[j])**(2)
        S_neg.append(round(math.sqrt(s),2))
        s=0
    return S_neg
def performance(r,S_pos,S_neg):
    per=[]
    for i in range(r):
        per.append(round(S_neg[i]/(S_neg[i]+S_pos[i]),2))
    return per
def main():
    print(sys.argv)
    if len(sys.argv)!=5:
        print("Error!! wrong number of parameters")
        print("Pass four parameters")
        print("example python ass6.py data.csv '1,1,1,1' '+,+,-,+' out.csv")
        exit(0)
    try:
        df=pd.read_csv(sys.argv[1])
        n_cols=len(df.columns)
        if n_cols<=2:
            print("Error!")
            print("pass at least three rows")
            sys.exit(0)
        weights=get_weight(sys.argv[2])
        impact=get_impact(sys.argv[3])
        for i in range(len(impact)):
            if impact[i]!="+" and impact[i]!="-":
                print("Error!")
                print("Impact is either + or -")
                sys.exit(0)
        num=num_col(df, n_cols)
        if len(weights)!=len(num) and len(impact)!=len(num):
            print("Error!")
            print("Pass correct number of weights and impact")
            sys.exit(0)
        non_num=non_num_col(df, num)
        df=weight_normalised(df, num,weights)
        V_pos=V_positive(df, num,impact)
        V_neg=V_negative(df, num,impact)
        fd=df.drop(non_num,axis=1)
        arr=fd.to_numpy()
        r=len(arr)
        c=len(arr[0])
        S_pos=S_positive(arr, r, c, V_pos)
        S_neg=S_negative(arr, r, c, V_neg)
        per=performance(r, S_pos, S_neg)
        fd['TOPSIS SCORE']=per
        fd['Rank'] = fd['TOPSIS SCORE'].rank(ascending=0)
        if os.path.isfile(sys.argv[4]):
            print("File already exists!!")
            print("Change the name of file")
            sys.exit(0)
        fd.to_csv(sys.argv[4])
    except:
        print("File not found!!")
        print("Make sure your files are present in same directory of program file!!")
if __name__=='__main__':
    main()