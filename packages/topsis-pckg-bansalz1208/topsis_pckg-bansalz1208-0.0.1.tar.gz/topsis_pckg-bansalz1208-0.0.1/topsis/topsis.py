import sys
import pandas as pd
if(len(sys.argv)!=5):
    raise Exception('there must be 5 arguments')
try:
    s=open(sys.argv[1])
except:
        raise Exception("Wrong file or file path")
df=pd.read_csv(sys.argv[1])
df2=pd.read_csv(sys.argv[1])
if(len(df.columns)<2):
    raise Exception('there must be more than 2 columns')
df1=df.dtypes
print(df1)
if(list(df1).count('float64')==df.shape[1]):
    raise Exception('there should be numeric values')
weight=[]
for i in sys.argv[2].replace('"','').split(','):
    weight.append(int(i))
if(len(df.columns[1:])!=len(weight)):
    raise Exception('the length of weight should be same with number of columns')
impact=[]
for i in sys.argv[3].replace('"','').split(','):
    impact.append(i)
if(len(df.columns[1:])!=len(weight)):
    raise Exception('the length of impact should be same with number of columns')
print(impact)
for i in impact:
    if(i!='+' and i!='-'):
        raise Exception('the impact should consist of + and -')
print(weight)
"""df=pd.read_csv("data.csv")
weight=[1,1,1,1]
impact=['+','+','+','+']"""
pd.set_option('mode.chained_assignment', None)
k=0
for i in df.columns[1:]:
    sum1=df[i].sum()
    for j in df.index:
        df.loc[j,i]=df.loc[j,i]/sum1
for i in df.columns[1:]:
    for j in df.index:
        df.loc[j,i]=df.loc[j,i]*weight[k]
    k+=1
val_plus=[]
val_minus=[]
k=0
for i in df.columns[1:]:
    if(impact[k]=='+'):
        val_plus.append(df[i].max())
        val_minus.append(df[i].min())
    else:
        val_minus.append(df[i].max())
        val_plus.append(df[i].min())
    k+=1
s_plus=[]
s_minus=[]
k=0
for i in df.index:
    temp1=0
    temp2=0
    k=0
    for j in df.columns[1:]:
        temp1+=(df[j][i]-val_plus[k])**2
        temp2+=(df[j][i]-val_minus[k])**2
        k+=1
    s_plus.append(temp1**0.5)
    s_minus.append(temp2**0.5)
perf=[]
for i in range(len(df.index)):
    perf.append(s_minus[i]/(s_minus[i]+s_plus[i]))
print(perf)
df2['Topsis score']=perf
list1=list(sorted(perf,reverse=True).index(x)+1 for x in perf)
df2['Rank']=list1
df2.to_csv(sys.argv[4], index=False)
