import pandas as pd 
import numpy as np

def topsis_rank(input_file,weights,impacts,output_file_name=None):
  input=pd.read_csv(input_file)
  weights=weights.split(',')
  weights=list(map(int,weights))
  impacts=impacts.split(',')

  labels=input.iloc[:,0]
  values=input.iloc[:,1:]
  values=np.array(values)
  for i in range(values.shape[1]):
    values[:,i]=values[:,i]/((values[:,i]**2).sum())

  values=values*weights
  
  max=[0]*(values.shape[1])
  min=[0]*(values.shape[1])
  for i in range(values.shape[1]):
    if impacts[i]=="+":
      max[i]=values[:,i].max()
      min[i]=values[:,i].min()
    elif impacts[i]=="-":
      max[i]=values[:,i].min()
      min[i]=values[:,i].max()

  max=np.array(max)
  min=np.array(min)

  s_plus=[0]*values.shape[0]
  s_minus=[0]*values.shape[0]
  for i in range(values.shape[0]):
    s_plus[i]=np.sqrt(((values[i]-max)**2).sum())
    s_minus[i]=np.sqrt(((values[i]-min)**2).sum())

  score=[0]*len(s_plus)
  for i in range(len(s_plus)):
    score[i]=s_minus[i]/(s_plus[i]+s_minus[i])

  output=input
  output['Topsis Score']=score
  output=output.sort_values(by='Topsis Score',ascending=False)

  output['Rank']=range(1,len(output)+1)

  output=output.sort_values(by=output.columns[0])

  if output_file_name!=None:
    output_file_name.to_csv(output_file_name,index=False)

  return output