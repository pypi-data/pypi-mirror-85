# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:36:35 2020

@author: Vinay Singh
"""
def topsis(filename,weights,impacts,resultfile):
  import pandas as pd
  import math


  try:
      df=pd.read_csv(str(filename))
  except:
      print("File Opening Error")
      exit()
  df=df.iloc[::,1:]

  if len(weights)<len(df.columns):
      print("Weights are not sufficient")
      exit()
  i=0
  for col in df.columns:
    df[col]=df[col]/math.sqrt((df[col]**2).sum())
    df[col]=df[col]*weights[i]
    i+=1


  worst_values=[]
  best_values=[]

  if len(impacts)<len(df.columns):
      print("Impacts are less than required")
      exit()

  k=0
  for col in df.columns:
    if impacts[k]=='-':
      best_values.append(df[col].min())
      worst_values.append(df[col].max())
    else:
      best_values.append(df[col].max())
      worst_values.append(df[col].min())
    k+=1

  mi=0
  ma=0
  neg=[]
  pos=[]
  for ind in df.index:
    j=0
    mi=0
    ma=0
    for col in df.columns:
      mi+=(df[col][ind]-worst_values[j])**2
      ma+=(df[col][ind]-best_values[j])**2
      j+=1
    neg.append(math.sqrt(mi))
    pos.append(math.sqrt(ma))
  df['S+']=pos
  df['S-']=neg
  df['T_score']=df['S-']/(df['S-']+df['S+'])
  df['Rank']=df['p_score'].rank(method='min',ascending=0)
  out=pd.read_csv(str(filename))
  out['T_score']=df['p_score']
  out['Rank']=df['Rank']
  print(out)
  out.to_csv(str(resultfile))
