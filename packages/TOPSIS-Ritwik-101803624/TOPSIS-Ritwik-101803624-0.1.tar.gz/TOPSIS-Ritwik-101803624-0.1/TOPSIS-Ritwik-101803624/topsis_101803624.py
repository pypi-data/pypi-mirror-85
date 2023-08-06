#Ritwik Sarkar - 101803624 - COE28
import sys
import numpy as np
from scipy.stats import rankdata
import argparse
import pandas as pd
import math
import os


#argument no check
if len(sys.argv) < 5:
	raise Exception("Invalid Number Of Arguments. Provide input data file (csv) , weights, impacts and output file(csv)")

#file type check
m = str(sys.argv[1]).split(".")
if m[1] not in ["csv"]:
	raise Exception('Provide CSV File as input File')

#file existence check
if not os.path.exists(sys.argv[1]):
	raise Exception(str(sys.argv[1])+" File not Found. Hint: Place it in same folder as .py file")



def topsi(df,impact,c):
    
    dataset = df.iloc[:,1:].values
    datas = dataset.tolist()
    
    rows= len(datas)
    
    positive =[]
    negative = []

    for i in range(0, len(datas[0])):
        sum=0
        
        for j in range(0,len(datas)):
            sum += datas[j][i]**2
            
        temp= math.sqrt(sum) 

        for j in range(0,len(datas)):
            datas[j][i]= datas[j][i]/temp
            datas[j][i]= datas[j][i]*c[i]
        
       
    for i in range(0, len(datas[0])):
        min = 100000000
        max = -100000000
        for j in range(0,len(datas)):
            if min > datas[j][i]:
                min= datas[j][i]
            if max < datas[j][i]:
                max = datas[j][i]
        if impact[i] == '+':
            positive.append(max)
            negative.append(min)
        if impact[i] == '-':
            positive.append(min)
            negative.append(max)
    
    spositive = []
    snegative = []
    performance = []
    
    for i in range(0,len(datas)):    
        sum=0
        sum1 = 0
        for j in range(0, len(datas[0])):
            sum = sum + (datas[i][j]-positive[j])*(datas[i][j]-positive[j])
            sum1 = sum1 + (datas[i][j]-negative[j])*(datas[i][j]-negative[j])
        sum = math.sqrt(sum)
        sum1 = math.sqrt(sum1)
        spositive.append(sum)
        snegative.append(sum1)
        
    for i in range(0,len(spositive)):
        performance.append(snegative[i]/(spositive[i]+snegative[i]))
        #print(performance)
    
    rank = len(performance) - rankdata(performance, method = 'min').astype(int) + 1
#     datas = np.column_stack((datas,performance,rank))
#     temp = datas   
    rank = rank.tolist()
    df["Topsis Score"] = performance
    df["Rank"] = rank
    return df
    
df = pd.read_csv(sys.argv[1])
dt = pd.read_csv(sys.argv[1])


changecol = len(df.columns[1:])
data_columns = df.columns[1:]
num_df = (df.drop(data_columns, axis=1)
         .join(df[data_columns].apply(pd.to_numeric, errors='coerce')))

num_df = num_df.dropna(how='all', axis=1)
data_columns = num_df.columns[1:]
changecol = changecol - len(data_columns)

values = {}
for i in data_columns:
  values[i] = num_df[i].mean()

df = num_df.fillna(value=values)

if changecol > 0:
	print("The input csv Data file has "+str(changecol)+" columns with all non-numeric values. So dropped the new processed data has "+str(len(df.columns)-1)+" columns. Verify it")

#check no of columns
noofcols = len(df.columns)
if noofcols < 3:
	raise Exception('Few Columns in Input csv File.Provide atleast 3 Columns in input csv file')

weights = sys.argv[2].split(',')
weights = [int(i) for i in weights]     

noofcols = noofcols - 1
#check weights
if noofcols != len(weights):
	print(len(weights))
	print(weights)
	print(noofcols)
	raise Exception('Invalid No of weights provided. HINT: The no of weights must be equal to ',str(noofcols))

total_weight = sum(weights)
result = map(lambda x: x/total_weight, weights)
weights = list(result)

impacts = sys.argv[3].split(',')

#checking type of data in impacts
count = 0
for i in impacts:
	if i=='+' or i=='-':
		count+=1

if count != len(impacts):
	raise Exception('The impacts contain iinvalid data. Impacts should contain only "+" or "-" in it')

#check impacts
if noofcols != len(impacts):
	raise Exception('Invalid No of impacts provided. HINT: The no of impacts must be equal to ',str(noofcols))
df = topsi(df,impacts,weights)
df.to_csv(sys.argv[4])



