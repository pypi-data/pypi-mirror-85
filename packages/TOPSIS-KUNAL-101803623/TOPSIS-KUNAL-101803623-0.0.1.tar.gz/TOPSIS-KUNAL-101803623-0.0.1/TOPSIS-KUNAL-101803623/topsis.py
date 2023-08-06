#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from scipy.stats import rankdata

def topsi(df,impact,c):
    
    dataset = df.iloc[:,1:].values
    datas = dataset.tolist()

    total_weight = sum(c)
    result = map(lambda x: x/total_weight,c)
    c = list(result)
    
    rows= len(datas)
    
    positive =[]
    negative = []

    for i in range(0, len(datas[0])):
        totalsum=0
        
        for j in range(0,len(datas)):
            totalsum += datas[j][i]**2
            
        temp= math.sqrt(totalsum) 

        for j in range(0,len(datas)):
            datas[j][i]= datas[j][i]/temp
            datas[j][i]= datas[j][i]*c[i]
        
       
    for i in range(0, len(datas[0])):
        min = 100000000
        max = -100000000
        for j in range(0,len(datas)):
            if min > datas[j][i]:
                min= datas[j][i]
            if max < datas[j][i]:
                max = datas[j][i]
        if impact[i] == '+':
            positive.append(max)
            negative.append(min)
        if impact[i] == '-':
            positive.append(min)
            negative.append(max)
    
    spositive = []
    snegative = []
    performance = []
    
    for i in range(0,len(datas)):    
        totalsum=0
        sum1 = 0
        for j in range(0, len(datas[0])):
            totalsum = totalsum + (datas[i][j]-positive[j])*(datas[i][j]-positive[j])
            sum1 = sum1 + (datas[i][j]-negative[j])*(datas[i][j]-negative[j])
        totalsum = math.sqrt(totalsum)
        sum1 = math.sqrt(sum1)
        spositive.append(totalsum)
        snegative.append(sum1)
        
    for i in range(0,len(spositive)):
        performance.append(snegative[i]/(spositive[i]+snegative[i]))
        #print(performance)
    
    rank = len(performance) - rankdata(performance, method = 'min').astype(int) + 1
#     datas = np.column_stack((datas,performance,rank))
#     temp = datas   
    rank = rank.tolist()
    df["Topsis Score"] = performance
    df["Rank"] = rank
    return df

