def topsis(filename,wts,imp,resultfilename):
  import pandas as pd
  import math


  try:
      df=pd.read_csv(str(filename))
  except:
      print("File Opening Error")
      exit()
  df=df.iloc[::,1:]
  lt=[]

  if len(wts)<len(df.columns):
      print("Weights are insufficient")
      exit()
  i=0
  for col in df.columns:
    df[col]=df[col]/math.sqrt((df[col]**2).sum())
    df[col]=df[col]*wts[i]
    i+=1


  mins=[]
  maxs=[]

  if len(imp)<len(df.columns):
      print("Impacts are insufficient")
      exit()

  k=0
  for col in df.columns:
    if imp[k]=='-':
      maxs.append(df[col].min())
      mins.append(df[col].max())
    else:
      maxs.append(df[col].max())
      mins.append(df[col].min())
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
      mi+=(df[col][ind]-mins[j])**2
      ma+=(df[col][ind]-maxs[j])**2
      #print(df[col][ind],maxs[j])
      j+=1
    neg.append(math.sqrt(mi))
    pos.append(math.sqrt(ma))
    #print(pos)
  df['S+']=pos
  df['S-']=neg
  df['p_score']=df['S-']/(df['S-']+df['S+'])
  df['rank']=df['p_score'].rank(method='min',ascending=0)
  out=pd.read_csv(str(filename))
  out['p_score']=df['p_score']
  out['rank']=df['rank']
  print(out)
  out.to_csv(str(resultfilename))
