import sys
import csv
import os
import math
import copy
import pandas as pd

#Enter location to input file
inp_data=sys.argv[1]

#checking if file exists
if (os.path.exists(inp_data)== False):
    print(inp_data+" file does not exist")
    exit(0)

#reading input file
inp_file=pd.read_csv(inp_data)

#calculating number of parameters
n_parameters=inp_file.shape[1]-1

if(n_parameters<3):
    print("number of columns are less than three")
    exit(0)


#contain weights and impacts passed in arguements
weights=[]
impacts=[]

#input weights
print("")
print("Provide the weights to features specified in input file")
print("weights can be inputed as integer as well as in decimal but not in fraction")
print("Adjacent weight should be seperated by commas")
inp_weight=input("WEIGHTS:")

#input impact
print("")
print("Provide the impacts that feature has on the TOPSIS value")
print("Impact can either be \"+\" or \"-\"")
print("Adjacent impacts should be seperated by commas")
inp_impact=input("IMPACTS:")

#input result file
print("")
result_file=input("Enter file name in which you want to store data along with its TOPSIS value and data:")

weight_length=len(inp_weight)
impact_length=len(inp_impact)


#creating weight list
i=0
while i!=weight_length:
    if(inp_weight[i]!=','):
        num=0
        cnt=0
        flag=0
        while(inp_weight[i]!=','):
            if(inp_weight[i]=='.'):
                if(flag==1):
                    print("used multiple decimal in single number")
                    exit(0)
                flag=1
                i+=1
                continue
            
            w=int(inp_weight[i])
            if(w>=0 and w<=9):
                num=num*10+w
                i+=1
                if(flag==1):
                    cnt+=1
                if(i==weight_length):
                    break
            else:
                print("weights aren't seperated by commas")
                exit(0)

        cnt=10**cnt
        num=num/cnt
        weights.append(num)
        
    elif(inp_weight[i]==','):
        i+=1
    else:
        print("weights aren't seperated by commas")
        exit(0)


#creating impact list
flag=0
for i in range (0,impact_length):
    if(inp_impact[i]=='+'):
        if(flag==1):
            print("found consecutive +/- operators without commas")
            exit(0)
        else:
            flag=1
            impacts.append(1)
    elif(inp_impact[i]=='-'):
        if(flag==1):
            print("found consecutive +/- operators without commas")
            exit(0)
        else:
            impacts.append(-1)
            flag=1
    elif(inp_impact[i]==','):
        if(flag==0):
            print("found consecutive commas")
            exit(0)
        else:
            flag=0
            continue
    else:
        print("impacts aren't in +/-")
        exit(0)


if(n_parameters!=len(weights)):
    print("Number of weights and number of columns (from 2nd to last columns) aren't same")
    exit(0)

if(n_parameters!=len(impacts)):
    print("Number of impacts and number of columns (from 2nd to last columns) aren't same")
    exit(0)


#total number of models    
n_models=inp_file.shape[0]

#column name of result.csv file
data_columns=list(inp_file.columns)

#coverting dataframe to list
inp_file=inp_file.values.tolist()

data=copy.deepcopy(inp_file)


#normalized performance value
for j in range(1,n_parameters+1):
    num=0
    for i in range (0,n_models):
        if(isinstance(inp_file[i][j], str)):
            print("data in the input file is not numeric")
            exit(0)
        else:
            num+=inp_file[i][j]*inp_file[i][j]
    num=math.sqrt(num)
    for i in range (0,n_models):
        inp_file[i][j]=inp_file[i][j]/num


#weighted normalized decision matrix
for j in range(1,n_parameters+1):
    for i in range (0,n_models):       
        inp_file[i][j]=inp_file[i][j] * weights[i-1]
        

#ideal best value and ideal worst value
ideal_best=[]
ideal_worst=[]

#calculating ideal best value and ideal worst value
for j in range(1,n_parameters+1):
    maxi=inp_file[0][j]
    mini=inp_file[0][j]
    for i in range (1,n_models):
        if(mini>inp_file[i][j]):
            mini=inp_file[i][j]
        if(maxi<inp_file[i][j]):
            maxi=inp_file[i][j]

    if(impacts[j-1]==1):
        ideal_best.append(maxi)
        ideal_worst.append(mini)
    else:
        ideal_best.append(mini)
        ideal_worst.append(maxi)
        

#Euclidean distance from ideal best value and ideal worst value
s_best=[]
s_worst=[]

#Calculate Euclidean distance from ideal best value and ideal worst value
for i in range(0,n_models):
    num1=0
    num2=0
    for j in range (1,n_parameters+1):
        num1+=(inp_file[i][j]-ideal_best[j-1])**2
        num2+=(inp_file[i][j]-ideal_worst[j-1])**2
    num1=math.sqrt(num1)
    num2=math.sqrt(num2)
    s_best.append(num1)
    s_worst.append(num2)
    

#Performance Score
performance=[]
temp_p=[]

#calculating performance score
for i in range (0,n_models):
    p=s_worst[i]/(s_best[i]+s_worst[i])
    performance.append(p)
    temp_p.append(p)


#rank list
rank=[]

#calculating rank
temp_p.sort(reverse=True)
for i in range (0,n_models):
    j=0
    while(temp_p[j]!=performance[i]):
        j+=1
    rank.append(j+1)


#data for result.csv file
result=[]
for i in range (0,n_models):
    l=[]
    for j in range(0,n_parameters+1):
        l.append(data[i][j])
    l.append(performance[i])
    l.append(rank[i])
    result.append(l)

#adding column name to result.csv file
data_columns.append("Topsis Score")
data_columns.append("Rank")


#creating result.csv file 
result_csv=open(result_file ,'x')

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

print("Done")
