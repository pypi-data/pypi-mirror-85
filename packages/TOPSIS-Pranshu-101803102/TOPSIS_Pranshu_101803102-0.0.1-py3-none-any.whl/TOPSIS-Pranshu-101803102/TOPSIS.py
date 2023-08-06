# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 2020

@author: Pranshu Goyal
"""
import os
import sys
import copy
import math
import pandas as pd

def check_csvfiles():
    y=[sys.argv[1],sys.argv[4]]
    for file in y:
        if not os.path.isfile(file):
            print(file," file doesn't exists")
            print("Recheck filename or directory and try again!")
            return False
        elif not file.endswith('.csv'):
            print(file,'is not in a csv file')
            print('Give a csv file only')
            return False
        else:
            pass
    return True

def check_col_colvalues():
    df=pd.read_csv(sys.argv[1])
    r=df.shape
    if r[1]<3:
        print("Minimum 3 no of columns are required")
    df=pd.read_csv(sys.argv[1])
    try:
        for i in range(0,r[0]):
            for j in range(1,r[1]):
                if str(df.iloc[i,j]).isnumeric() or float(df.iloc[i,j]):
                    pass
                else:
                    print("Values are not numeric from 2nd to last column")
        return False    
    except:
        print("Values are not numeric from 2nd to last column")
        return True
    
def verify():
    for i in range(len(sys.argv[2])):
        if i+1!=',':
            print("values are not separated by commas")
            return True
        else:
            pass
    for i in range(len(sys.argv[3])):
        if i+1!=',':
            print("values are not separated by commas")
            return True
        else:
            pass
    return False

def main():
  try:
    df=pd.read_csv(sys.argv[1])
    df1=copy.deepcopy(df)
    y=df.shape
    z=[]
    k=y[0]
    m=y[1]
    for j in range(1,m):
        x=0
        for i in range(0,k):
            y=df.iloc[i,j]*df.iloc[i,j]
            x=x+y
        z.append(math.sqrt(x))
    l=0
    for j in range(1,m):
        for i in range(0,k):
            df.iloc[i,j]=df.iloc[i,j]/z[l];
        l=l+1;
    w=[]
    for i in sys.argv[2]:
        if i==',':
            pass
        else:
            w.append(int(i,0))
    l=0
    for j in range(1,m):
        for i in range(0,k):
            df.iloc[i,j]=df.iloc[i,j]*w[l];
        l=l+1;
    vmax=[]
    vmin=[]
    impact=[]
    for i in sys.argv[3]:
        if i==',':
            pass
        elif i=="+" or i=='-':
            impact.append(i);
        else:
            raise Exception("Impact values are not + or -")
    
    k=0
    for j in range(1,m): 
        if impact[k]=='-':
            vmax.append(min(df.iloc[:,j]))
            vmin.append(max(df.iloc[:,j]))
            k=k+1
        else:
            vmax.append(max(df.iloc[:,j]))
            vmin.append(min(df.iloc[:,j]))
            k=k+1
    smax=[]
    smin=[]
    for i in range(0,k+1):
        x=0
        l=0
        for j in range(1,m):
            p=(df.iloc[i,j]-vmax[l])*(df.iloc[i,j]-vmax[l])
            x=x+p
            l=l+1
        smax.append(math.sqrt(x))
    for i in range(0,k+1):
        x=0
        l=0
        for j in range(1,m):
            p=(df.iloc[i,j]-vmin[l])*(df.iloc[i,j]-vmin[l])
            x=x+p
            l=l+1
        smin.append(math.sqrt(x))
    smaxmin=[]
    for i in range(len(smax)):
        smaxmin.append(smax[i]+smin[i])
    perform=[]
    for i in range(len(smax)):
        perform.append(smin[i]/smaxmin[i])
    df1.insert(m,"Topsis Score",perform)
    r=[]
    for i in range(0,k+1):
        r.append(0)
    l=1
    while(l!=k+2):
        y=max(perform)
        for i in range(len(perform)):
            if perform[i]==y:
                r[i]=l
                l=l+1
                perform[i]=0
                break
    df1.insert(m+1,"Rank",r)
    df1.to_csv(sys.argv[4],index=False)
  except FileNotFoundError:
    print(" file doesn't exists")
    print("Recheck filename or directory and try again!")
  except:
    if len(sys.argv)<5:
        print("Minimum five parameters are required")
    elif not check_csvfiles():
        pass
    elif check_col_colvalues():
        pass
    elif verify():
        pass
    elif IndexError:
        print("Length  are not same")
    else:
        print("Something went wrong try again")
        
if __name__=="__'main'__":
    main()


