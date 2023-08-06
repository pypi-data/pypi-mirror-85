#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from scipy.stats import rankdata
import numpy as np

def topsi(df,impact,c):
    data=df.iloc[:,1:].values
    data_norm=data/(np.sqrt(np.power(data,2).sum(axis=0)))
    data_norm_w=data_norm*c
    
    positive =[]
    negative = []
        

    
    for i in range(0, len(data_norm_w[0])):
        min = 100000000
        max = -100000000
        for j in range(0,len(data_norm_w)):
            if min > data_norm_w[j][i]:
                min= data_norm_w[j][i]
            if max < data_norm_w[j][i]:
                max = data_norm_w[j][i]
        if impact[i] == '+':
            positive.append(max)
            negative.append(min)
        if impact[i] == '-':
            positive.append(min)
            negative.append(max)
            
    sm_p=np.sqrt(np.power(data_norm_w-positive,2).sum(axis=1))
    sm_n=np.sqrt(np.power(data_norm_w-negative,2).sum(axis=1))
    performance=sm_n/(sm_n+sm_p)
    
    rank = len(performance) - rankdata(performance, method = 'min').astype(int) + 1
 
    rank = rank.tolist()
    df["Topsis Score"] = performance
    df["Rank"] = rank
    return df
