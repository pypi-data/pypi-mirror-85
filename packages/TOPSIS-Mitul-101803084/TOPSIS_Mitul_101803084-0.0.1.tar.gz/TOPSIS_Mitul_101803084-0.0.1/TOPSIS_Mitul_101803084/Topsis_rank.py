import pandas as pd 
import numpy as np

class Topsis_rank():

  def __init__(self,input_file,weights,impacts,output_file_name=None):
    try:
      self.input_file=pd.read_csv(input_file)
    except FileNotFoundError:
      self.input_file=None
      print("File not found or Wrong path")
      exit()

    file=self.input_file.iloc[:,1:]
    if file.select_dtypes(include=['number','int','float']).shape[1]!=file.shape[1]:
      print("Convert these categorical columns into numerical: "+str(file.select_dtypes(include=['object']).columns))
      self.input_file=None
      exit()

    self.weights=weights.split(',')
    try:
      gotdata = self.weights[1]
    except IndexError:
      print("Impacts not seprated by comma")
      exit()

    if len(self.weights)!=(self.input_file.shape[1]-1):
      print("Too few impacts provided.Provide "+str(self.input_file.shape[1]-1)+" impacts")
      exit()

    self.weights=list(map(int,self.weights))

    self.impacts=impacts.split(',')
    try:
      gotdata = self.impacts[1]
    except IndexError:
      print("Impacts not seprated by comma")
      exit()

    for i in self.impacts:
      if i=='+' or i=='-':
        continue
      else:
        print("Impacts can only be '+' or '-'.")
        exit()
    if len(self.impacts)!=(self.input_file.shape[1]-1):
      print("Too few impacts provided.Provide "+str(self.input_file.shape[1]-1)+" impacts")
      exit()
    
    self.output_file_name=output_file_name

  def calculate_rank(self):
    labels=self.input_file.iloc[:,0]
    values=self.input_file.iloc[:,1:]
    values=np.array(values)
    for i in range(values.shape[1]):
      values[:,i]=values[:,i]/((values[:,i]**2).sum())
  
    values=values*(self.weights)
    
    max=[0]*(values.shape[1])
    min=[0]*(values.shape[1])
    for i in range(values.shape[1]):
      if self.impacts[i]=="+":
        max[i]=values[:,i].max()
        min[i]=values[:,i].min()
      elif self.impacts[i]=="-":
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

    output=self.input_file
    output['Topsis Score']=score
    output=output.sort_values(by='Topsis Score',ascending=False)

    output['Rank']=range(1,len(output)+1)

    output=output.sort_values(by=output.columns[0])

    if self.output_file_name!=None:
      output.to_csv(self.output_file_name,index=False)

    return output

