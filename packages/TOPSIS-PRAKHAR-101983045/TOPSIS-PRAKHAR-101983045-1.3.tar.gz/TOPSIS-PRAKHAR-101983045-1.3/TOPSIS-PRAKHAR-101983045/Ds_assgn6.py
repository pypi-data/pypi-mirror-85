
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:14:58 2020

@author: prakhar
"""

import sys,pandas as pd
import logging
def topsis(sys1,sys2,sys3,sys4):
    
    if sys1[-4:]!='.csv':
        logging.warning("Please enter a '.csv' file as input. ")
        return(0)
    try:
        df=pd.read_csv(sys1)
    except:
         logging.warning("File not found ")
         return(0)
        
    
    ifile=sys1
    wts=list(map(int, sys2.split(',')))
    imps=list(sys3.split(','))

    
    print(df)
    if len(wts)!=len(imps):
        logging.warning("Error. Number of Weights and Impacts are different.")
        return
    for i in imps:
        if i!='+' and i!='-':
            logging.warning("Error. Please enter '+' or '-' only for Impacts . ")
            return
    if len(df.columns)<3:
        logging.warning("Error. Less than three columns in input file.")
        return
    if (len(df.columns)-1) != len(wts):
        logging.warning("Error. Number of Weights and Attributes are unequal.")
        return
    for i in df.dtypes[1:]:
        if i!="float64":
            logging.warning("Input file contains non numeric values. Please try again.")
            return
    
   
    rs=[]
    for i in df.columns[1:]:
        total=0
        for j in list(df[i]):
            total+=(j**2)
        rs.append(total**(0.5))
    for index,i in enumerate(df.columns[1:]):
        for j in df[i]:
            df[i]=df[i].replace(j,j*wts[index]/rs[index])
    
    vlist=[]
    for index,i in enumerate(df.columns[1:]):
        if imps[index]=='-':
            vp=min(df[i])
            vn=max(df[i])
        else:
            vp=max(df[i])
            vn=min(df[i])
        
        vlist.append((vp, vn))
        
    
    n=len(df.index)
    tops=[]
    for i in range(n):
        sp=0
        sn=0
        for index,j in enumerate(list(df.iloc[i])[1:]):
            sp+=((j-vlist[index][0])**2)
            sn+=((j-vlist[index][1])**2)
        sp=(sp)**0.5
        sn=(sn)**0.5
        tops.append(sn/(sp+sn))
        
    final=pd.read_csv(ifile)
    final['Topsis']=tops
    final["Rank"]=final["Topsis"].rank(ascending=0)
    
    print(final)
    result=sys4
    final.to_csv(result)





