import pandas as pd
import numpy as np
import sys
if len(sys.argv)!=5:
  print("InCorrect number of parameters")
  exit(0)

def changeArr(input1):  
    newArray = input1[:]  
    newArray.sort(reverse=True)
    ranks = {}  
    rank = 1
    for index in range(len(newArray)):  
        element = newArray[index]
        if element not in ranks:  
            ranks[element] = rank  
            rank += 1
    for index in range(len(input1)):  
        element = input1[index]  
        input1[index] = ranks[input1[index]] 
def topsis():
  file_name=sys.argv[1]
  weights=sys.argv[2]
  impacts=sys.argv[3]
  result_fileName=sys.argv[4]
  try:
    weights=[float (x) for x in weights.split(",")]
  except:
    print("Weights not comma seperated")
    exit(0)  

  try:
    impacts=impacts.split(",")
  except:
    print("Impacts not comma seperated")
    exit(0) 
  for chk in impacts:
    if chk!="+" and chk!="-":
      print("Impacts must be either +ve or -ve")
      exit(0)

  try:
    df=pd.read_csv(file_name)
  except:
    print("File not Found")
    exit(0)
  col_names=list(df)
  no_of_cols=len(col_names)
  if (no_of_cols-1)!=len(weights) or (no_of_cols-1)!=len(impacts) or len(weights)!=len(impacts):
    print("Number of weights, number of impacts and number of columns from 2nd to last columns are not equal")
    exit(0)

  no_of_rows=len(list(df[col_names[0]]))


  #calculating v+ and v-
  spos=[0]*no_of_rows
  sneg=[0]*no_of_rows
      
  for curr in range(1,no_of_cols):
      li=list(df[col_names[curr]])
      sum_of_squares=0
      for ele in li:
          try:
            sum_of_squares+=(ele**2)
          except:
            print("Non-numeric values are present in column number",curr+1)
            exit(0)
      square_root=sum_of_squares**(0.5)
      
      #normalization
      for i in range(len(li)):
          li[i]=(li[i]/square_root)*weights[curr-1]
          
      if impacts[curr-1]=="+":
          vpos=max(li)
          vneg=min(li)
      else:
          vpos=min(li)
          vneg=max(li)
      
      for i in range(len(spos)):
          spos[i]+=((li[i]-vpos)**2)
          
      for i in range(len(sneg)):
          sneg[i]+=((li[i]-vneg)**2)
      
          

  for i in range(len(spos)):
      spos[i]=(spos[i]**0.5)
  for i in range(len(sneg)):
      sneg[i]=(sneg[i]**0.5)

  spos_plus_sneg=[0]*no_of_rows
  for i in range(len(spos_plus_sneg)):
      spos_plus_sneg[i]=spos[i]+sneg[i]

  preformance_score=[0]*no_of_rows

  for i in range(len(preformance_score)):
      preformance_score[i]=sneg[i]/spos_plus_sneg[i]

  rank=preformance_score[:]
  changeArr(rank)
  df["Topsis Score"]=preformance_score
  df["Rank"]=rank
  df.set_index(col_names[0],inplace = True)
  df.to_csv(result_fileName)




if __name__ == '__main__':
  topsis()
