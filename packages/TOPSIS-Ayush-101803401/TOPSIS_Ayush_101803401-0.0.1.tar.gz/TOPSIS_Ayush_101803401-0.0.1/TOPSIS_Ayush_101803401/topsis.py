import pandas as pd
import math as m
from pandas.api.types import is_numeric_dtype
import sys
a=sys.argv[1]
if(a[-4:]!='.csv'):
    print('FILE IS NOT OF CSV TYPE')
    exit(0)
try:
        dataset_original=pd.read_csv(sys.argv[1])
        dataset=pd.read_csv(sys.argv[1])
        #print(dataset)
except:
    print('FILE NOT FOUND ')
    exit(0)
if(len(sys.argv)!=5):
    print('Incorrect number of parameters passed')
    exit(0)
i,j=dataset.shape
if(j<3):
    print('Input file contains less than 3 columns')
    exit(0)
t=dataset.columns
for u in range(1,len(t)):
    if not (is_numeric_dtype(dataset.iloc[:,u])):
        print('column contains non numeric value')
        exit(0)
count_col=len(t)-1    
weights=sys.argv[2]
impacts=sys.argv[3]
count_weights=0
for u in range(0,len(sys.argv[2])):
    if(sys.argv[2][u]!=','):
        count_weights+=1
count_impacts=0
for u in range(0,len(sys.argv[3])):
    if(sys.argv[3][u]!=','):
        count_impacts+=1
if(count_weights!=count_col or count_weights!=count_impacts):
    print('Number of weights ,columns and impacts are not same')
    exit(0)
check_impact=0
for u in range(0,len(sys.argv[3])):
    if(sys.argv[3][u]=='+'or sys.argv[3][u]=='-'):
        continue
    elif(sys.argv[3][u]==','):
        continue
    else:
        check_impact+=1
if(check_impact!=0):
    print('values in impact are other than + or -')
    exit(0)
check_comm_weights=0
for u in range(1,len(sys.argv[2]),2):
    if(sys.argv[2][u]!=','):
        check_comm_weights+=1
if(check_comm_weights!=0):
    print('weights are not separated by commas ')
    exit(0)
check_comm_impacts=0
for u in range(1,len(sys.argv[3]),2):
    if(sys.argv[3][u]!=','):
        check_comm_impacts+=1
if(check_comm_impacts!=0):
    print('impacts are not separated by commas ')
    exit(0)   

vpos=[]
vneg=[]
spos=[]
sneg=[]
weight1=[]
impact1=[]
spos_sneg=[]
rank_list=[]
performance_score=[]
for u in range(0,len(sys.argv[2]),2):
    weight1.append(int((sys.argv[2][u])))
for u in range(0,len(sys.argv[3]),2):
    impact1.append((sys.argv[3][u]))
print(dataset)
print('-----------------------------------')
result=[]
for k in range(1,i):
    sum=0
    for l in range(0,j):
        sum+=dataset.iloc[l,k]*dataset.iloc[l,k]
    sum=m.sqrt(sum)
    result.append(sum)
for k in range(1,i):
    for l in range(0,j):
        dataset.iloc[l,k]=dataset.iloc[l,k]/result[k-1]
print('normalized matrix becomes')
print(dataset)
for k in range(1,i):
    for l in range(0,j):
        dataset.iloc[l,k]=dataset.iloc[l,k]*weight1[k-1]
for o in range(1,len(impact1)+1):
    if(impact1[o-1]=='+'):
        vpos.append(max(dataset.iloc[:,o]))
    else:
        vpos.append(min(dataset.iloc[:,o]))
for o in range(1,len(impact1)+1):
    if(impact1[o-1]=='+'):
        vneg.append(min(dataset.iloc[:,o]))
    else:
        vneg.append(max(dataset.iloc[:,o]))
print('v positive becomes ',vpos)
print('v negative becomes ',vneg)
for p in range(0,i):
    sum=0
    for k in range(1,j):
        sum+=(dataset.iloc[p,k]-vpos[k-1])*(dataset.iloc[p,k]-vpos[k-1])
    spos.append(m.sqrt(sum))
for p in range(0,i):
    sum=0
    for k in range(1,j):
        sum+=(dataset.iloc[p,k]-vneg[k-1])*(dataset.iloc[p,k]-vneg[k-1])
    sneg.append(m.sqrt(sum))

print('s positive becomes ',spos)
print('s negative becomes ',sneg)
for u in range(0,len(spos)):
    spos_sneg.append(spos[u]+sneg[u])
for u in range(0,len(spos)):
    performance_score.append(sneg[u]/(spos[u]+sneg[u]))
print('topsis_score becomes ',performance_score)
performance_score=pd.Series(performance_score)
dataset_original['Topsis_score']=performance_score
dataset_original['Rank']=dataset_original['Topsis_score'].rank(ascending=0)
result=sys.argv[4]
dataset_original.to_csv(result)
print('final dataset=')
print(dataset_original)
print('succesfully created file')