import sys
from os import path
import pandas as pd
import numpy as np
import scipy.stats as ss

def topsis(input,w,i,output_file):
    input_file = pd.read_csv(input)
    n = len(input_file.columns)
    length = len(input_file)
    df = input_file
    for j in range(1,n):
        s = np.sqrt(np.square(df.iloc[:,j]).sum())
        p = df.iloc[:,j]/s
        p = p*w[j-1]
        m = df.columns[j]
        df[m] = p

    v_best=[]
    v_worst=[]
    for j in range(1,n):
        if (i[j-1]=="+"):
            ma = max(df.iloc[:,j])
            v_best.append(ma)
            mi = min(df.iloc[:,j])
            v_worst.append(mi)
        elif (i[j-1]=="-"):
            ma = max(df.iloc[:,j])
            v_worst.append(ma)
            mi = min(df.iloc[:,j])
            v_best.append(mi)

    s_plus = []
    s_minus = []
    for j in range(0,length):
        maxi=0
        mini=0
        for k in range(1,n):
            maxi += (np.square(df.iloc[j,k] - v_best[k-1]))
            mini += (np.square(df.iloc[j,k] - v_worst[k-1]))
        s_plus.append(np.sqrt(maxi))
        s_minus.append(np.sqrt(mini))
    performance = []
    for j in range(0,length):
        performance.append(s_minus[j]/(s_minus[j]+s_plus[j]))
    rank = ss.rankdata(performance)
    rank1 = len(performance) - rank.astype(int) +1
    d = pd.read_csv(input)
    d["Topsis Score"] = performance
    d["Rank"] = rank1
    d.to_csv("result.csv")

def main():
    input_file = pd.read_csv(sys.argv[1])
    input = sys.argv[1]
    weight = sys.argv[2]
    impact = sys.argv[3]
    output = sys.argv[4]
    
           
    if len(sys.argv)!=5:
        print("Enter correct number of parameters")
        exit(0)
    if not(sys.argv[1].endswith(".csv") or sys.argv[4].endswith(".csv")):
        print("Wrong inputs entered")
        exit(0)
    if not(path.exists(input) or path.exists(output)):
        print("File not Found")
        exit(0)
    if (len(input_file.columns) <=3):
        print("Columns less than expected")
        exit(0)
    k=0
    for i in input_file.columns:
        k=k+1
        for j in input_file.index:
            if k!=1:
                val = isinstance(input_file[i][j],int)
                val1 = isinstance(input_file[i][j],float)
                if not val and not val1:
                    print(f"Value is not numeric in {k} column")
                    exit(0)
                
    n = len(input_file.columns)
    i=[]
    w = []
    i = impact.split(",")
    w = weight.split(",")
    
    for j in range(len(w)):
        w[j] = float(w[j])
    if not(len(w) == len(i) == n-1):
        print("No. of weights, no. of impacts, no. of columns from second are not equal")
        exit(0)
    
    
    if not("+" or "-" in i):
        print("impact must contain only + or -")
        exit(0)
    if(len(i)<=1 and len(w)<=1):
        print("Either weights or impacts are not comma separated")
        exit(0)
    topsis(input,w,i,output)

if __name__=='__main__':
    main()

