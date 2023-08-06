import pandas as pd
import math as m
import sys
import os


l=['py','data.csv','1,2,1,1',"+,+,-,+",'final.csv']
l=l[1:]
if len(l)!=4:
    print('Wrong entries: <inputDataFile> <wts> <im> <ResultFileName>!! try again')
    exit()


directory = os.getcwd()
files=list(os.listdir(directory))
if l[0] not in files:
    print('file not found in current location : '+str(directory))
    exit()

    
df=pd.read_csv(l[0],index_col=0)
leng=len(df.columns)
df.reset_index()
df2=df.copy()


w=l[1].split(",")
wt=[float(i) for i in w]
im=l[2].split(",")

vp=[]
vm=[]
for x in range(leng):
    sqsos=m.sqrt(sum(map(lambda i : i * i, df.iloc[:,x])))

    norm=list(map(lambda i : i/sqsos, df.iloc[:,x])) 
    
    wnval=list(map(lambda i : i*wt[x-1], norm))
    df2.iloc[:,x]=wnval
    
    if im[x]=="-": 
        vp.append(min(df2.iloc[:,x]))   
        vm.append(max(df2.iloc[:,x])) 
    else: 
        vp.append(max(df2.iloc[:,x]))   
        vm.append(min(df2.iloc[:,x])) 

sp1=[]
sm=[]
sc=[]

def sp (l,vp):  
    return(l-vp)**2


for x in df2.values:
    splus=m.sqrt(sum(map(sp,x,vp)))
    
    sminus=m.sqrt(sum(map(sp,x,vm)))
    
    score=sminus/(splus+sminus)

    sp1.append(splus)
    sm.append(sminus)
    sc.append(score)
df2['s+']=sp1
df2['s-']=sm
df2['score']=sc
df2=df2.sort_values('score',ascending=False) 
name=l[3]
df2.to_csv(name)
print('done')
