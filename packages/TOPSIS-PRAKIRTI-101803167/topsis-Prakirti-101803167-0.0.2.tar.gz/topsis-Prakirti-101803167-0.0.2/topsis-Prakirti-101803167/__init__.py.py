import pandas as pd
import copy
import sys
import numpy as np

if __name__ == "__main__":


    d=pd.read_csv(sys.argv[1])
    num=len(d.columns)
        

    w = sys.argv[2]
    imp = sys.argv[3]

    weights = []
    impacts = []

    for i in range(0,len(imp)):
        if imp[i] == ',':
            continue;
        impacts.append(imp[i])
        

    n = ''
    for i in range(0,len(w)):
        if w[i] == ',':
            weights.append(float(n))
            n = ''
            continue
        n = n + w[i]

    weights.append(float(n))


    df=pd.read_csv(sys.argv[1])
    df22=df[df.columns[1:]]
    df2=copy.deepcopy(df22)
        
    for i in df22.columns:
        df22[i]=df22[i]**2

    sum_column=df22.sum(axis=0)
    sum_column=sum_column**0.5

    j=0
    for i in df2.columns:
        df2[i]=df2[i]/sum_column[j]
        j+=1

    sum_weights=sum(weights)
    weights=[i/sum_weights for i in weights]

       
        
    j=0
    for i in df2.columns:
        df2[i]=df2[i]*weights[j]
        j+=1

    ideal_best=[]
    ideal_worst=[]

    j=0
    for i in df2.columns:
        if impacts[j]=='+':
            ideal_best.append(max(df2[i]))
            ideal_worst.append(min(df2[i]))
        else:
            ideal_best.append(min(df2[i]))
            ideal_worst.append(max(df2[i]))
            
        j+=1

        
    df3=copy.deepcopy(df2)
    df4=copy.deepcopy(df2)

    j=0
    for i in df3.columns:
        df3[i]=(df3[i]-ideal_best[j])
        j+=1

    j=0
    for i in df3.columns:
        df3[i]=(df3[i])**2
        j+=1

    j=0
    for i in df4.columns:
        df4[i]=(df4[i]-ideal_worst[j])
        j+=1

    j=0
    for i in df4.columns:
        df4[i]=(df4[i])**2
        j+=1

    number=len(df4.columns)
    euclidean_worst=df4.sum(axis=1)
    euclidean_best=df3.sum(axis=1)

        


    for i in range(0,len(euclidean_worst)):
        euclidean_worst[i] = np.sqrt( euclidean_worst[i])

    for i in range(0,len( euclidean_worst)):
        euclidean_best[i] =  np.sqrt(euclidean_best[i])

    ps = []

        
    for i in range(0,len(euclidean_worst)):
        t = euclidean_worst[i] + euclidean_best[i]
        ps.append(t)
        
    performance_score=[]
    for i in range(0,len(euclidean_worst)):
        t = euclidean_worst[i]/ps[i]
        performance_score.append(t)

    df['Topsis Score']=performance_score
    df['Rank']=df['Topsis Score'].rank(ascending = 0)

    df.set_index(df.columns[0],inplace=True)

    df.to_csv(sys.argv[4])
        
    

    



