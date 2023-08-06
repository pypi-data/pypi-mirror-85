import pandas as pd
import os
import sys
import math
import copy
import re
from os import path
from pandas.api.types import is_numeric_dtype

#reading the file
#os.chdir("/Users/mishaaggarwal/Desktop/Data_Science /Assignment06 - TOPSIS/Input files for Assignment06")

def main():
    
    l = []
    j = 0
    sum = []
    pos = []    #IDEAL BEST 
    neg = []    #IDEAL WORST
    
    
    n = sys.argv
    length = len(n)
    if(length != 5):                            #CHECK NO. OF INPUTS
        print("Wrong number of inputs")
        return 
    
    a = 0                                       #inputs should be comma seperated 
    for i in range(2,4):
        while (a < len(n[i])):
            test=n[i]
            test_list = test.split(',')
            try:
                numbers = [str(x.strip()) for x in test_list]
            except:
                print('please try again, commas separated input (e.g. "1, 5, 3")')
                continue
            else:
                #print(numbers)
                break
            a+=1
            
    if (path.exists(n[1])):                     #FILE EXITS OR NO
        if n[1].endswith('.csv') and n[4].endswith('.csv'):  #1st and 4th input is a .csv file or not
            a+=1
        else:
            print("Error with input arguments")
            return
    else:
        raise Exception("file not found")
        
    
    #original Dataframe
    dfF = pd.read_csv(n[1])
    #copied Dataframe
    df = copy.deepcopy(dfF)
    df1 = copy.deepcopy(df)
    df2 = copy.deepcopy(df)
    impact = (re.findall("[+-]+", n[3]))        #impact i/p, this will only choose "+" or "-"
    temp = re.findall(r'\d+', n[2])             # weight i/p, this will choose only integer values    
    w = list(map(int, temp))
    
    
    number_of_columns = len(df.columns)
    
    if(number_of_columns < 3 ):                 #number of columns in input datafile
        print("Input file has less than 3 columns")
        return 
    
    number_of_columns -= 1                      #CORRECT INPUTS 
    if(len(impact) != number_of_columns):       #correct input for IMPACTS 
        print("Invalid Impact values")
        return 
    
    if(len(w) != number_of_columns):            #correct input for WEIGHTS 
        print("Invalid Impact values")
        return 
    
    
    for col in df.columns:      #COLUMN NAMES
        l.append(col)
        for i in l[1:]:
            if(is_numeric_dtype(df[i])):
                a+=1
            else:
                raise Exception("2nd to last columns of input file contains values other than numeric values")
    
    
    #extracting data
    for i in l[1:]:
        T = 0
        
        for line in df[i]:              #find col-wise rms
            T = T + (line*line)
        T = math.sqrt(T)
        sum.append(T)
        
        df[i] = (df[i]/sum[j]) * w[j]   #Normalized
        
                                            
        if(impact[j] == "+"):           #Weight Matrix
            pos.append(max(df[i]))
            neg.append(min(df[i]))
        elif(impact[j] == "-"):
            pos.append(min(df[i]))
            neg.append(max(df[i]))
        j+=1
    
    
    #S COLUMN
    j = 0
    for i in l[1:]:
        df1[i] = (df[i] - pos[j])*(df[i] - pos[j])
        df2[i] = (df[i] - neg[j])*(df[i] - neg[j])
        j+=1
    df["s+"] = df1.sum(axis=1)
    df["s-"] = df2.sum(axis=1) 
    
    
    df["sum"] = df["s+"] + df["s-"]    #SUM OF S COLUMNS 
    dfF["Score"] = df["s-"]/df["sum"]   #TOPSIS SCORE    
    dfF["Rank"] = dfF["Score"].rank(ascending=False)    #RANK
    
    print(dfF)
    
    
       
if __name__ == "__main__":
    main()














