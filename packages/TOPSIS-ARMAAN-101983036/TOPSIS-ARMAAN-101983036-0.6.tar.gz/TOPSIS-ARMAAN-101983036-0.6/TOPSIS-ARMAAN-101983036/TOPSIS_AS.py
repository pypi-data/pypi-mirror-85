# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:55:59 2020

@author: Armaan
"""
def topsis(sys1,sys2,sys3,sys4):
    
    import pandas as pd
    import math as m
    from pandas.api.types import is_numeric_dtype
    import logging
    import sys
    a=sys1
    if(a[-4:]!='.csv'):
        logging.warning('FILE IS NOT OF CSV TYPE')
        return
    try:
        dataset_original=pd.read_csv(sys1)
        dataset=pd.read_csv(sys1)
        #print(dataset)
    except:
        logging.warning('FILE NOT FOUND ')
        return
    i,j=dataset.shape
    if(j<3):
        logging.warning('Input file contains less than 3 columns')
        return
    t=dataset.columns
    for u in range(1,len(t)):
        if not (is_numeric_dtype(dataset.iloc[:,u])):
            logging.warning('column contains non numeric value')
            return
    count_col=len(t)-1    
    weights=sys2
    impacts=sys3
    count_weights=0
    for u in range(0,len(sys2)):
        if(sys2[u]!=','):
            count_weights+=1
    count_impacts=0
    for u in range(0,len(sys3)):
        if(sys3[u]!=','):
            count_impacts+=1
    if(count_weights!=count_col or count_weights!=count_impacts):
        logging.warning('Number of weights ,columns and impacts are not same')
        return
    check_impact=0
    for u in range(0,len(sys3)):
        if(sys3[u]=='+'or sys3[u]=='-'):
            continue
        elif(sys3[u]==','):
            continue
        else:
            check_impact+=1
    if(check_impact!=0):
        logging.warning('values in impact are other than + or -')
        return
    check_comm_weights=0
    for u in range(1,len(sys2),2):
        if(sys2[u]!=','):
            check_comm_weights+=1
    if(check_comm_weights!=0):
        logging.warning('weights are not separated by commas ')
        return
    check_comm_impacts=0
    for u in range(1,len(sys3),2):
        if(sys3[u]!=','):
            check_comm_impacts+=1
    if(check_comm_impacts!=0):
        logging.warning('impacts are not separated by commas ')
        return   
    vpos=[]
    vneg=[]
    spos=[]
    sneg=[]
    weight1=[]
    impact1=[]
    spos_sneg=[]
    rank_list=[]
    performance_score=[]
    for u in range(0,len(sys2),2):
        weight1.append(int((sys2[u])))
    for u in range(0,len(sys3),2):
        impact1.append((sys3[u]))
    logging.warning(dataset)
    logging.warning('-----------------------------------')
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
    logging.warning('normalized matrix becomes')
    logging.warning(dataset)
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
    logging.warning('v positive becomes ',vpos)
    logging.warning('v negative becomes ',vneg)
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

    logging.warning('s positive becomes ',spos)
    logging.warning('s negative becomes ',sneg)
    for u in range(0,len(spos)):
        spos_sneg.append(spos[u]+sneg[u])
    for u in range(0,len(spos)):
        performance_score.append(sneg[u]/(spos[u]+sneg[u]))
    logging.warning('topsis_score becomes ',performance_score)
    performance_score=pd.Series(performance_score)
    dataset_original['Topsis_score']=performance_score
    dataset_original['Rank']=dataset_original['Topsis_score'].rank(ascending=0)
    result=sys4
    dataset_original.to_csv(result)
    logging.warning('final dataset=')
    logging.warning(dataset_original)
    logging.warning('succesfully created file')
