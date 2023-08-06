import numpy as np
import pandas as pd
import sys
from os.path import isfile

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print('Incorrect number of parameters.')

    else:
        f = sys.argv[1].split('.')
        e = f[-1]
        if e!='csv':
            print('File must be of csv type.')
        else:
            if isfile(sys.argv[1])==False:
                print('File not Found.')
            else:
                df = pd.read_csv(sys.argv[1])
                if len(df.columns)<3:
                    print('File must contain three or more columns')
                else:
                    df = pd.read_csv(sys.argv[1])
                    df1 = df[df.columns[1:]]
                    count=0
                    for i in range(len(df1.columns)):
                        if pd.to_numeric(df1[df1.columns[i]], errors='coerce').notnull().all() == False:
                            count+=1
                    if count>0:
                        print('2nd to last columns must contain numeric values only.')
                    else:
                        weights = (sys.argv[2]).split(',')
                        for i in range(len(weights)):
                            weights[i]=int(weights[i])
                        impacts = (sys.argv[3]).split(',')
                        if len(weights)!= len(impacts):
                            print('Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same')
                        else:
                            rms = []
                            for i in range(len(df1.columns)):
                                s=0
                                for j in range(len(df1.iloc[:,i])):
                                    s += df1.iloc[j,i]**2
                                rms.append(np.sqrt(s/len(df1.iloc[:,i])))
                            vp=[]
                            vm=[]
                            sp=[]
                            sm=[]
                            tsis=[]
                            
                            df2 = pd.DataFrame()
                            for i in range(len(df1.columns)):
                                new=[]
                                for j in range(len(df1.iloc[:,i])):
                                    new.append(df1.iloc[j,i]/rms[i])
                                df2[i] = new
                            for i in range(len(df2.columns)):
                                df2[i]*=(weights[i]/sum(weights))
                            for i in range(len(impacts)):
                                if impacts[i] == '+':
                                    vp.append(max(df2[i]))
                                    vm.append(min(df2[i]))
                                elif impacts[i] == '-':
                                    vp.append(min(df2[i]))
                                    vm.append(max(df2[i]))
                       
                            rows, columns = df2.shape
                            for i in range(rows):
                                xp = 0
                                xm = 0
                                for j in range(columns):
                                    xp+=(df2.iloc[i,j]-vp[j])**2
                                    xm+=(df2.iloc[i,j]-vm[j])**2
                                sp.append(np.sqrt(xp))
                                sm.append(np.sqrt(xm))
                         
                            for i in range(len(sp)):
                                tsis.append(sm[i]/(sm[i]+sp[i]))
                            
                            df['Topsis Score']=tsis
                            df['Topsis Score'] = df['Topsis Score'].round(2)
                            df['Rank']=df['Topsis Score'].rank(ascending=0)
                            rank=[]
                            for i in df['Rank']:
                                i = int(i)
                                rank.append(i)
                            df['Rank']=rank
                        
                            del(f,e, df1,df2,s,new,rms,vp,vm,xp,xm,sm,sp,tsis,count,weights,impacts,rows,columns,i,j,rank)
                      
                            df.to_csv(sys.argv[4], index=False)