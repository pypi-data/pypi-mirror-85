import pandas as pd
import numpy as np
import sys
from os import path
if len(sys.argv)!=5:
    raise Exception("Wrong number of parameters.")
if not path.exists(sys.argv[1]):
    raise Exception("File doesn't exist. Please select another file.")
d=pd.read_csv(sys.argv[1])
data=pd.DataFrame(d)
data=data.values[:,1:]
if len(data[0])<3:
    raise Exception("Insufficient number of columns.")
##if not np.core.defchararray.isnumeric(data).all():
  ##  raise Exception("Values not numeric.")
try:
    data = pd.DataFrame(data).to_numpy(dtype = float)
except:
    exit()
weights=pd.Series(sys.argv[2].split(",")).astype(float)
v=list(sys.argv[3].split(","))
if len(data[0])!=len(weights):
    print(len(data[0]),len(weights))
    raise Exception("Column mismatch for weights.")
if len(data[0])!=len(v):
    raise Exception("Column mismatch for impacts.")
##Finding weighted normalized decision matrix
col_sq=[]
for i in range(len(data[0])):
    s=0
    for j in range(len(data)):
        s=s+data[j][i]**2
    s=pow(s,0.5)
    col_sq.append(s)
for i in range(len(data[0])):
    for j in range(len(data)):
        data[j][i]=data[j][i]*weights[i]/col_sq[i]
v_p=[]
v_n=[]
k=0
##Calculating ideal best and ideal worst value 
for i in range(len(data[0])):
    if v[k]=='+':
        v_p.append(np.amax(data, axis=0)[i])
        v_n.append(np.amin(data, axis=0)[i])
    else:
        v_n.append(np.amax(data, axis=0)[i])
        v_p.append(np.amin(data, axis=0)[i])
    k=k+1
##Finding euclidean distance from ideal best and ideal worst values
min_euc=[]
max_euc=[]
for i in range(len(data)):
    s_min=0
    s_max=0
    for j in range(len(data[0])):
        s_max=s_max+(data[i][j]-v_p[j])**2
        s_min=s_min+(data[i][j]-v_n[j])**2
    max_euc.append(pow(s_max,0.5))
    min_euc.append(pow(s_min,0.5))
##calculating performance score
per_score=[]
for i in range(len(min_euc)):
    per_score.append(min_euc[i]/(min_euc[i]+max_euc[i]))
rank=pd.Series(per_score).rank()
final=pd.DataFrame({'Topsis score':per_score,'Rank':rank})
pd.concat([d,final],axis=1).to_csv(sys.argv[4],index=False)