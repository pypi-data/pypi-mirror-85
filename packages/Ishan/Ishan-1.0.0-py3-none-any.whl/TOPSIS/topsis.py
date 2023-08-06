import sys
import csv
import pandas as pd
import os
import copy

para_num=len(sys.argv)

if para_num!=5:
    print("Incorrect number of paramters")
    exit(0)

inputData=sys.argv[1]

try:
    s=open(inputData)
except FileNotFoundError:
    raise Exception("File doesn't exist")        
        
data=pd.read_csv(inputData)
x,y=data.shape
if y<3:
    raise Exception("File with three or more column is valid only!")


inp_weight=sys.argv[2]
inp_impact=sys.argv[3]
weight=[]
impact=[]

for i in range(len(inp_weight)):
    if i%2!=0 and inp_weight[i]!=',':
        print("Weights aren't seperated by commas")
        exit(0)
    if i%2==0:
        num=int(inp_weight[i])
        weight.append(num)

for i in range(len(inp_impact)):
    if i%2!=0 and inp_impact[i]!=',':
        print("Impacts aren't seperated by commas")
        exit(0)
    if i%2==0:
        if inp_impact[i]=='+' or inp_impact[i]=='-':
            impact.append(inp_impact[i])
        else:
            print("Impact is neither +ve or -ve")
            exit(0)

if y-1!=len(weight):
    print("Number of weight and columns (from 2nd to last column) aren't same")
    exit(0)

if y-1!=len(impact):
    print("Number of impact and columns (from 2nd to last column) aren't same")
    exit(0)

data_columns=list(data.columns)
data=data.values.tolist()
c_data=copy.deepcopy(data)

#normalized performance value
for i in range(1,y):
    sum=0
    for j in range(x):
        if(isinstance(data[j][i], str)):
            print("Data in the input file is not numeric")
            exit(0)
        else:
            sum=sum+data[j][i]**2
    sum=sum**0.5
    for k in range(x):
        data[k][i]=data[k][i]/sum

#weighted normalized decision matrix
for i in range(1,y):
    for j in range(x):
        data[j][i]=data[j][i]*weight[i-1]

#ideal best value and ideal worst value
i_best=[]
i_worst=[]

#calculating ideal best and worst for every feature/column
for i in range(1,y):
    maxi=data[0][i]
    mini=data[0][i]
    for j in range(x):
        if data[j][i]>maxi:
            maxi=data[j][i]
        if data[j][i]<mini:
            mini=data[j][i]
    if impact[i-1]=='+':
        i_best.append(maxi)
        i_worst.append(mini)
    else:
        i_best.append(mini)
        i_worst.append(maxi)

#Euclidean distance from ideal best value and ideal worst value
s_best=[]
s_worst=[]

#Calculating euclidean distance for each feature/column
for i in range(x):
    sum1=0
    sum2=0
    for j in range(1,y):
        sum1=sum1+(data[i][j]-i_best[j-1])**2
        sum2=sum2+(data[i][j]-i_worst[j-1])**2
    sum1=sum1**0.5
    sum2=sum2**0.5
    s_best.append(sum1)
    s_worst.append(sum2)
    
performance_score=[]
temp_score=[]
#Calculating performance score for each data row
for i in range(x):
    score=s_worst[i]/(s_best[i]+s_worst[i])
    performance_score.append(score)
    temp_score.append(score)

temp_score.sort(reverse=True)

#Calculating the ranking 
rank=[]
for i in range(x):
    for j in range(x):
        if(performance_score[i]==temp_score[j]):
            rank.append(j+1)

result=[]
for i in range (x):
    l=[]
    for j in range(y):
        l.append(c_data[i][j])
    l.append(performance_score[i])
    l.append(rank[i])
    result.append(l)

#adding column name to result.csv file
data_columns.append("Topsis Score")
data_columns.append("Rank")

#creating result.csv file 
result_csv=open(sys.argv[4],'x')
#giving column names to csv file                  
fields=data_columns
#creating a csv writer object                    
csvwriter = csv.writer(result_csv)
#writing the fields                  
csvwriter.writerow(fields)
#writing the data rows
csvwriter.writerows(result)
#closing log csv file
result_csv.close()

print()
print("Result file containing all the input columns, TOPSIS SCORE and RANK is ready!")