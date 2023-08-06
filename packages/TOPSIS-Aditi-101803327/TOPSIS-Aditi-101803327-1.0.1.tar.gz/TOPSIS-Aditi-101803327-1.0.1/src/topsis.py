# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:49:07 2020

@author: Aditi Dona
"""

import pandas as pd
import  numpy as np
import sys
import math

def main():
    
    # Checking for correct number of parameters 
    if(len(sys.argv)!=5):
        print('Invalid number of arguments')
        sys.exit()
    
    # Checking of the input file exists 
    dataFile =sys.argv[1]
    try:
        df = pd.read_csv(dataFile)
    except:
        print(dataFile+' File not found');
        sys.exit()
    # Checking is the table has correct number of columns
    cols=df.shape[1]
    if df.shape[1]<3:
      print('Invalid !, number of columns are less than 3')
      exit(1)
        
    # Checking if weights and impacts are in correct format    
    weights = sys.argv[2]
    impacts = sys.argv[3]
    try:
        weights=list(weights.split(','))
        impacts=list(impacts.split(','))
        weights=[float(i) for i in weights]
    except:
        print('Invalid format for weights or impacts')
        sys.exit()
    
    for i in impacts :
        if i not in ('+','-'):
            print('Impacts not in proper format ')
            sys.exit()
    
    # Checking if lengths of weights and impacts are correct     
    data=df.iloc[:,1:]
    if len(weights)!=data.shape[1] or len(impacts)!=data.shape[1]:
      print('Length of weights and Length of impacts is not equal to the number of columns')
      sys.exit()
                
    targetFile = sys.argv[4]
    
    # vector normalisation    
    data=data.astype(float)
    
    root_of_sum_of_squares=[]
    for i in range(data.shape[1]):
      col=np.array(data.iloc[:,i])
      col=col*col
      root_of_sum_of_squares.append(math.sqrt(col.sum()))
      
    for i in range(0,data.shape[0]):
      for j in range(0,data.shape[1]):
        data.loc[i][j]=(data.loc[i][j]/root_of_sum_of_squares[j])*weights[j]
        
    #Finding ideal_best and ideal worst value
    ideal_best=[]
    ideal_worst=[]
    for i in range(len(impacts)):
      col=np.array(data.iloc[:,i])
      if impacts[i] == '+':
        ideal_best.append(col.max())
        ideal_worst.append(col.min())
      elif impacts[i] == '-':
        ideal_best.append(col.min())
        ideal_worst.append(col.max())
        
    # Calculating Eucledian Distance
    pos_dis=[]
    neg_dis=[]
    for i in range(data.shape[0]):
      row=np.array(data.iloc[i,:])
      best=np.array([])
      worst=np.array([])
      best=(row-ideal_best)**2
      worst=(row-ideal_worst)**2
      dis_pos=best.sum()
      dis_neg=worst.sum()
      pos_dis.append(math.sqrt(dis_pos))
      neg_dis.append(math.sqrt(dis_neg))

    # Calculating Performance Score
    perf_score=[]
    sum_of_pos_neg=[]
    for i in range(len(pos_dis)):
      sum_of_pos_neg.append(pos_dis[i]+neg_dis[i])
    
    for i in range(len(neg_dis)):
      perf_score.append(neg_dis[i]/sum_of_pos_neg[i])
      
    # rank
    rank=[]
    sort=sorted(perf_score,reverse=True)
    for i in perf_score:
      rank.append(sort.index(i)+1)
    
    #updating the table
    out=df
    out['Topsis Score']=perf_score
    out['Rank']=rank
    
    #saving the output
    out.to_csv(targetFile,index=False)
    
# calling the main function
if __name__=="__main__": 
    main()
    

    
