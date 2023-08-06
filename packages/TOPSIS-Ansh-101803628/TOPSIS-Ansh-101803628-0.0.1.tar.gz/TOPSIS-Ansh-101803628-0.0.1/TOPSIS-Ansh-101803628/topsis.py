#Ansh Bangia
#101803628
#COE 28

import pandas as pd
import math
import os
import sys
import numpy as np
from scipy.stats import rankdata
import argparse

def topsis(df,impacts,weights):
        data=df.iloc[:,1:].values.tolist()
        rows=len(data)
        pos=[]
        neg=[]
        for i in range(len(data[0])):
                sum=0
                for j in range(len(data)):
                        sum+=data[j][i]**2
                temp=math.sqrt(sum)
                for j in range(len(data)):
                        data[j][i]/=temp
                        data[j][i]*=weights[i]
        for i in range(len(data[0])):
                min=sys.maxsize
                max=-sys.maxsize
                for j in range(len(data)):
                        if data[j][i]<min:
                                min= data[j][i]
                        if data[j][i]>max:
                                max=data[j][i]
                if impacts[i]=='+':
                        pos.append(max)
                        neg.append(min)
                if impacts[i]=='-':
                        pos.append(min)
                        neg.append(max)
        sp=[]
        sn=[]
        performance=[]
        for i in range(len(data)):
                sum=0
                sum2=0
                for j in range(len(data[0])):
                        sum+=(data[i][j]-pos[j])*(data[i][j]-pos[j])
                        sum2+=(data[i][j]-neg[j])*(data[i][j]-neg[j])
                sum=math.sqrt(sum)
                sum2=math.sqrt(sum2)
                sp.append(sum)
                sn.append(sum2)
        for i in range(len(sp)):
                performance.append(sn[i]/(sp[i]+sn[i]))
        rank=len(performance)-rankdata(performance,method='min').astype(int)+1
        rank=rank.tolist()
        df["Topsis Score"]=performance
        df["Rank"]=rank
        return df

if len(sys.argv)<5:
        print('Invalid input format.')
        print('Correct input format: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>')
else:
        m = str(sys.argv[1]).split(".")
        if m[1] not in ["csv"]:
                print('Input data file should be of csv format.')
        else:
                if not os.path.exists(sys.argv[1]):
                        print('File not found. Keep the input data file in the same folder as topsys.py file.')
                else:
                        df=pd.read_csv(sys.argv[1])
                        dt=pd.read_csv(sys.argv[1])
                        changecolumn=len(df.columns[1:])
                        columnsData=df.columns[1:]
                        df_num=(df.drop(columnsData,axis=1).join(df[columnsData].apply(pd.to_numeric,errors='coerce')))
                        df_num=df_num.dropna(how='all',axis=1)
                        columnsData=df_num.columns[1:]
                        changecolumn=changecolumn-len(columnsData)
                        vals={}
                        for i in columnsData:
                                vals[i]=df_num[i].mean()
                        df=df_num.fillna(value=vals)
                        if changecolumn>0:
                                print('The input data file has ',(changecolumn),' columns with all non-numeric values.')
                                print('The new processed data has ',len(df.columns)-1,' columns.')
                        col_num=len(df.columns)
                        if col_num<3:
                                print('Input data file should have atleast 3 columns of data.')
                        else:
                                weights=sys.argv[2].split(',')
                                weights=[int(i) for i in weights]
                                col_num-=1
                                if col_num!=len(weights):
                                        print('The number of weights should be equal to ',col_num,'.')
                                else:
                                        weightTotal=sum(weights)
                                        weights=list(map(lambda x: x/weightTotal,weights))
                                        impacts=sys.argv[3].split(',')
                                        count=0
                                        for i in impacts:
                                                if i=='+' or i=='-':
                                                        count+=1
                                        if count!=len(impacts):
                                                print('The impacts should contain only "+" or "-" in it.')
                                        else:
                                                if col_num!=len(impacts):
                                                        print('The number of impacts should be equal to ',col_num)
                                                else:
                                                        df=topsis(df,impacts,weights)
                                                        df.to_csv(sys.argv[4],index=False)
                                                        print('Procedure successful. Check result file.')
                                                        









