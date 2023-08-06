import sys
import pandas as pd
import numpy as np
if len(sys.argv)<5:
    print('Incorrect number of parameters.')
    sys.exit()
datafile=sys.argv[1]
weights=sys.argv[2]
impact=sys.argv[3]
result_data=sys.argv[4]
try:
    weights=list(map(float,weights.split(',')))
    impact=list(map(str,impact.split(',')))
except:
    print('Incorrect format of Weights or Impacts.')
    sys.exit()
for i in impact:
    if i not in ('+','-'):
        print('Incorrect Input for Impacts.')
        sys.exit()
try:
    data=pd.read_csv(datafile)
except:
    print(datafile+' file not found.')
    sys.exit()
if len(list(data.columns))<=2:
    print('Input Data file should contain 3 or more columns.')
    sys.exit()
data=pd.read_csv(datafile)
datalist=data.values.tolist()
for i in datalist:
    i.remove(i[0])
datalist1=data.values.tolist()
if len(weights)!=len(datalist[0]):
    print('Incorrect number of weights.')
if len(impact)!=len(datalist[0]):
    print('Incorrect number of Impacts.')
ideal_best,ideal_worst,norm=[],[],[]
for i in range(len(datalist[0])):
    sum=0
    for j in datalist:
        sum+=j[i]**2
    norm.append(sum**0.5)
z=np.sum(weights)
weights=[i/z for i in weights]
for i in range(len(datalist[0])):
    for j,jata in enumerate(datalist):
        datalist[j][i]/=norm[i] 
        datalist[j][i]*=weights[i]
    if impact[i]=='+':
        max,min=-1,10**10
        for j,jata in enumerate(datalist):
            if jata[i]>max:
                max=jata[i]
            if jata[i]<min:
                min=jata[i]
        ideal_best.append(max)
        ideal_worst.append(min)
    if impact[i]=='-':
        max,min=-1,10**10
        for j,jata in enumerate(datalist):
            if jata[i]>max:
                max=jata[i]
            if jata[i]<min:
                min=jata[i]
        ideal_best.append(min)
        ideal_worst.append(max)           
sp,sm=[],[]
for j in datalist:
    a,b=0,0
    for k,kata in enumerate(j):
        a+=(kata-ideal_best[k])**2
        b+=(kata-ideal_worst[k])**2
    sp.append(a)
    sm.append(b)     
for i in range(len(datalist1)):
    datalist1[i].append(sm[i]/(sp[i]+sm[i]))
p=[datalist1[i][-1] for i in range(len(datalist))]
p.sort()
for i,iata in enumerate(datalist1):
    datalist1[i].append(p.index(iata[5])+1)
datalist1.insert(0,['Model','Corr','Rseq','RMSE','Accuracy','Tospis Score','Rank'])
result=pd.DataFrame(datalist1)
result.to_csv(result_data,index=True)
