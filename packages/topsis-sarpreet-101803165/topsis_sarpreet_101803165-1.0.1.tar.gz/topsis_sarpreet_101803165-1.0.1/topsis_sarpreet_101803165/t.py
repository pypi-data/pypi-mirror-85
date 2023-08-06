#!/usr/bin/env python
# coding: utf-8

# In[8]:
import sys
import pandas as pd
import math
    
import os
def topsis(inputname,weight,impact,output):
   



    def string(string):
        l=list(string.split(","))
        return l
    try:
        file=pd.read_csv(inputname)
    except:
        print("wrong input file")
    rows=file.shape[0]
    cols=file.shape[1]
    if cols<3:
        raise Exception("error!! no of columns is less than 3","wrong input file")
    for i in range(rows):
        for j in range(1,cols):
            if str(file.iloc[i,j]).isalpha()==True:
                raise Exception("error!!all values are not numeric","wrong input file")
    p=[]

    sp=[]
    sm=[]
    vjm=[0]
    try:
        impact=string(impact)
    except:
        print("impact not separated by commas")


    weight=string(weight)




    for i in range(len(impact)):
        if impact[i]=='+' or impact[i]=='-':
            pass
        else:
            raise Exception("impact not given properly")
            break

    if not len(weight)==(cols-1) and not len(impact)==(cols-1):
        raise Exception("error!!number of weights/impacts is not equal to no. of columns","wrong inputs given")

    vjp=[0]
    for j in range(1,cols):

        v1=0
        sum=0
        c1=[]
        for i in range(len(file)):

            c1.append(file.iloc[i,j])
        for i in range(len(c1)):
            sum=sum+c1[i]*c1[i]
        v1=math.sqrt(sum)

        for i in range(len(c1)):
            c1[i]=c1[i]/v1
            try:
                c1[i]=c1[i]*float(weight[j-1])
            except:
                print("weights not separated by commas")
                sys.exit(0)
            file.iloc[i,j]=c1[i]

        if impact[j-1]=='+':
            vjp.append(max(c1))
            vjm.append(min(c1))
        if impact[j-1]=='-':
            vjp.append(min(c1))
            vjm.append(max(c1))

    for i in range(rows):
        s1=0
        s2=0
        for j in range(1,cols):
            s1=s1+((file.iloc[i,j]-vjp[j])*(file.iloc[i,j]-vjp[j]))
            s2=s2+((file.iloc[i,j]-vjm[j])*(file.iloc[i,j]-vjm[j]))
        sp.append(math.sqrt(s1))
        sm.append(math.sqrt(s2))
    for i in range(len(sm)):
        p.append(sm[i]/(sp[i]+sm[i]))
    file2=pd.read_csv("data.csv")

    file2['topsis_score']=p
    file2['rank']=file2['topsis_score'].rank(method='dense',ascending=False)
    file2.to_csv(output)

   
    





