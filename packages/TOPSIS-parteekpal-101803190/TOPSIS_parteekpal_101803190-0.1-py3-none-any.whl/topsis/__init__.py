from sys import float_repr_style
import pandas as pd
import numpy as np
import sys
def topsis(arg1,arg2,arg3,arg4):
 try:
  df=pd.read_csv(f"{arg1}")
  df=pd.DataFrame(df)
 except:
    print("File Not Found!!")
    sys.exit()
 

 if(len(df.columns)<3):
   print("Incompatible Input File!!")
   sys.exit()

 check=[]
 for i in df.columns[1:]:
    check.append(i)
    
 for i in check:
    for j in df[f'{i}']:
        if(isinstance(j,float)==False):
            sys.exit()
 l=list()
 for col in df.columns:
    s=0.00
    
    if col!=df.columns[0]:
        for row in range(len(df)):
            s+=float(df[col][row]**2)
        s=np.sqrt(s)
        l.append(s)    

 weights=[]
 for i in arg2:
    if(i!=','):
     weights.append(int(i))
 for i in weights:
    pass
 if((len(df.columns)-1)!=len(weights)):
    print('Argument Error!!')
    sys.exit()
 count=0
 for col in df.columns:
    if col!=df.columns[0]:
        df[col]=df[col].div(l[count])
        m=float(weights[count])
        df[col]=df[col]*m
        count+=1

 impacts=[]
 for i in arg3:
    if(i!=','):
        impacts.append(i)
 if((len(df.columns)-1)!=len(impacts)):
    print('Argument Error!!')
    sys.exit()
 a1=list()
 b1=list()
 count=0
 for col in df.columns:
    if col!=df.columns[0]:
        if impacts[count]=='+':
            a1.append(max(df[col]))
            b1.append(min(df[col]))
        else:
            b1.append(max(df[col]))
            a1.append(min(df[col]))
        count+=1 

 s1=list()
 s2=list()
 for row in range(len(df)):
    count=0
    s3=0.00
    s4=0.00
    for col in df.columns:
        if col!=df.columns[0]:
            s3=s3+float((df[col][row]-a1[count])**2)
            s4=s4+float((df[col][row]-b1[count])**2)
            count+=1
    s1.append(np.sqrt(s3))
    s2.append(np.sqrt(s4))

 p=list()
 for i in range(len(df)):
    p.append(s2[i]/(s1[i]+s2[i]))
 df['Topsis Score']=p
 r=list()
 for i in range(len(df)):
    r.append(len(df)-i)
 df.sort_values(by='Topsis Score',inplace=True)
 df['Rank']=r
 df['index']=df.index
 df.sort_values(by='index',inplace=True)
 df.drop(columns='index',inplace=True)
 f1=open(f'{arg4}',"w")
 df.to_csv(f1,index=False)

