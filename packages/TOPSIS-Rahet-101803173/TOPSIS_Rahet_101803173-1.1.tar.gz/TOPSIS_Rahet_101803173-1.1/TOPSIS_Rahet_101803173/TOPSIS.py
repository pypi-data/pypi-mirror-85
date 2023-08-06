import pandas as pd
import  numpy as np
import sys
import math as m
if len(sys.argv) < 5:
    print('NOT ENOUGH ARG')
    sys.exit()

fileName = sys.argv[1]
weightage = sys.argv[2]
weightage = weightage.split(",")
weightage = [float(i) for i in weightage] 
#print(weightage)

impact = sys.argv[3]
impact = impact.split(",")
#print(impact)

resultFile = sys.argv[4]
#print(resultFile)

dataset = pd.read_csv(fileName)
#print(dataset)
data=dataset.iloc[ :,1:].values.astype(float)

(r,c)=data.shape

s=sum(weightage)

if len(weightage) != c:
    print("INSUFFICIENT WEIGHTS")
    sys.exit()

for i in range(c):
    weightage[i]/=s


a=[0]*(c)


for i in range(0,r):
    for j in range(0,c):
        a[j]=a[j]+(data[i][j]*data[i][j])

for j in range(c):
    a[j]=m.sqrt(a[j])


for i in range(r):
    for j in range(c):
        data[i][j]/=a[j]
        data[i][j]*=weightage[j]


ideal_positive=np.amax(data,axis=0) 
ideal_negative=np.amin(data,axis=0) 
for i in range(len(impact)):
    if(impact[i]=='-'):        
        temp=ideal_positive[i]
        ideal_positive[i]=ideal_negative[i]
        ideal_negative[i]=temp

dist_pos=list()
dist_neg=list()

for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-ideal_positive[j]), 2)

    dist_pos.append(float(pow(s,0.5)))


for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-ideal_negative[j]), 2)

    dist_neg.append(float(pow(s,0.5)))


performance_score=dict()

for i in range(r):
    performance_score[i+1]=dist_neg[i]/(dist_neg[i]+dist_pos[i])

a=list(performance_score.values())
b=sorted(list(performance_score.values()) , reverse=True)

rank=dict()

for i in range(len(a)):
    rank[(b.index(a[i]) + 1)] = a[i]
    b[b.index(a[i])] =-b[b.index(a[i])]


row=list(i+1 for i in range(len(b)))
a=list(rank.values())
rr=list(rank.keys())
out={'Row_NO':row,'Performance_score' : a , 'Rank':rr}
output=pd.DataFrame(out)
#print(output)
dataset.drop(dataset.columns[0], axis=1)
dataset.to_csv(resultFile,index = False)
#print(dataset)
df = pd.read_csv(resultFile)
df["Topsis Score"] = a
df.to_csv(resultFile, index=False)
df["Rank"] = rr
df.to_csv(resultFile, index=False)

