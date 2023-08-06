'''
Name -> Aman Sharma
Batch -> COE7
Roll No -> 101803676
Assignment 6 - Topsis
'''

import sys
import pandas as pd
import math
import copy

def main():
    if len(sys.argv)!=5: # Checks if right number of arguments are given
        print('Not right number of parameters!')
        exit(0)
    
    file = sys.argv[1]
    try: # This try except checks if a file is present or not
        df = pd.read_csv(file)
    except FileNotFoundError:
        print('This file is not present')
        exit(0)
        
    if len(df.columns)<3:
        print("Number of columns should be 3 or more")
        exit(0)
        
    df2 = copy.deepcopy(df)
    
    # Vector Normalization
    r = []
    for i in range(1,len(df2.columns)):
        sum = 0
        for j in df2[df2.columns[i]]:
            sum = sum+j**2
        r.append(math.sqrt(sum))
        df2[df2.columns[i]] = df2[df2.columns[i]]/math.sqrt(sum)
        
    # Weight Assignment
    w = sys.argv[2].split(',')
    if len(w)!=len(df.columns)-1:
        print("Length of weights is not equal to columns")
        exit(0)
    if any(char.isalpha() for char in w)==True:
        print("Only numbers are allowed as weights!")
        exit(0)
    for i in range(1,len(df2.columns)):
        df2[df2.columns[i]] = df2[df2.columns[i]]*int(w[i-1])
    
    # Finding ideal best and ideal worst
    I = sys.argv[3].split(',')
    if len(I)!=len(df.columns)-1:
        print("Length of impacts is not equal to columns")
        exit(0)
    vjp = []
    vjn = []
    for i in range(1,len(df2.columns)):
        if I[i-1]=='+':
            vp = max(df2[df2.columns[i]])
            vn = min(df2[df2.columns[i]])
        elif I[i-1]=='-':
            vp = min(df2[df2.columns[i]])
            vn = max(df2[df2.columns[i]])
        else:
            print('Impact can be only + or -')
            exit(0)
        vjp.append(vp)
        vjn.append(vn)
        
    # Calculating Euclidean distance
    sp = []
    sn = []
    for i in range(len(df2)):
        sump = 0
        sumn = 0
        for j in range(1,len(df2.columns)):
            sump = sump+(df2.loc[i][j]-vjp[j-1])**2
            sumn = sumn+(df2.loc[i][j]-vjn[j-1])**2
        sp.append(math.sqrt(sump))
        sn.append(math.sqrt(sumn))
        
    # Calculating Performance Score
    p = []
    for i in range(len(sp)):
        p.append(sn[i]/(sn[i]+sp[i]))
    
    df['Topsis Score'] = p
    p2 = copy.deepcopy(p)
    p2 = sorted(p2,reverse=True)
    rank = []
    for i in p:
        for j in range(len(p2)):
            if i==p2[j]:
                rank.append(j+1)
    
    df['Rank'] = rank
    df.to_csv(sys.argv[4],index=False)
    print(sys.argv[4] + ' created!')

if __name__ == '__main__':
    main()
    
           
    
        
        
        
        
        
        
        
        
        
        
        