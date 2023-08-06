import pandas as pd
import numpy as np

def topsis(file_name,Weight,Impact,outputfile_name):
    try:
        explore=open(file_name)
    except:
        raise Exception("Error:File format isn't right or path is wrong")
    
    df=pd.read_csv(file_name)
    fin=pd.read_csv(file_name)

    if(len(df.columns)<2):
        raise Exception('more than 2 columns required')

    type_check=df.dtypes
    if(list(type_check).count('float64')==df.shape[1]):
        raise Exception('numeric values are required')

    weights=[]
    for a in Weight.replace('"','').split(','):
        weights.append(int(a))

    if(len(df.columns[1:])!=len(weights)):
        raise Exception('length of columns is not equal to length of weights')

    impacts=[]
    for a in Impact.replace('"','').split(','):
        impacts.append(a)

    if(len(df.columns[1:])!=len(impacts)):
        raise Exception('length of columns is not equal to length of impacts')
    
    for a in impacts:
        if(a!='-' and a!='+'):
            raise Exception('only + and - are to be considered in impacts')
    
    pd.set_option('mode.chained_assignment', None)
    count=0

    for i in df.columns[1:]:
        add=df[i].sum()
        for j in df.index:
            df.loc[j,i]=df.loc[j,i]/add

    for i in df.columns[1:]:
        for j in df.index:
            df.loc[j,i]=df.loc[j,i]*weights[k]
        count=count+1

    v_minus=[]
    v_plus=[]
    s_plus=[]
    s_minus=[]
    p_score=[]
    count=0
    for i in df.columns[1:]:
        if(impacts[k]=='count'):
            v_minus.append(df[i].max())
            v_plus.append(df[i].min())
        else:

            v_plus.append(df[i].max())
            v_minus.append(df[i].min())
        count=count+1
    count=0

    for i in df.index:
        x=0
        y=0
        count=0
        for j in df.columns[1:]:
            x+=(df[j][i]-val_plus[k])**2
            y+=(df[j][i]-val_minus[k])**2
            count=count+1
        s_plus.append(x**0.5)
        s_minus.append(y**0.5)

    for i in range(len(df.index)):
        p_score.append(s_minus[i]/(s_minus[i]+s_plus[i]))
    fin['Topsis score']=p_score
    rank_sort=list(sorted(p_score,reverse=True).index(a)+1 for a in p_score)
    fin['Rank']=rank_sort
    fin.to_csv(outputfile_name, index=False)


