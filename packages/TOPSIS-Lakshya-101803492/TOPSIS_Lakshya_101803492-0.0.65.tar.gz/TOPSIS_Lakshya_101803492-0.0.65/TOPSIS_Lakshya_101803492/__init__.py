#!/usr/bin/env python
# coding: utf-8

"""
@author: Lakshya Gupta
"""

import pandas as pd
import numpy as np
import sys

def calcTopsis(df,weights,impacts):
    m=df.shape[0] #Number of rows
    n=len(df.columns) #Number of columns
    
    #Find root of sum of squares of each column
    rootsum=[0]
    for i in range(1,n):
        temp=0
        for j in df.iloc[:,i]:
            temp=temp+pow(j,2)
        rootsum.append(pow(temp,0.5))
        
    #Divide each element by the above value for each column
    for i in range(1,n):
        counter=0
        for j in df.iloc[:,i]:
            df.iloc[counter,i]=df.iloc[counter,i]/rootsum[i]
            counter+=1
    
    #Calculate weights
    for i in range(1,n):
        weights[i-1]=float(weights[i-1])
        
    #Multiply each value by respective weights
    for i in range(1,n):
        counter=0
        for j in df.iloc[:,i]:
            df.iloc[counter,i]=df.iloc[counter,i]*weights[i-1]
            counter+=1

    #Calculate ideal best and ideal worst values
    vbest=[0]
    vworst=[0]
    for i in range(1,n):
        if impacts[i-1]=='+':
            vbest.append(df.iloc[:,i].max())
            vworst.append(df.iloc[:,i].min())
            
        elif impacts[i-1]=='-':
            vbest.append(df.iloc[:,i].min())
            vworst.append(df.iloc[:,i].max())

    #Find euclidean distances from best and worst values   
    sbest=[]
    sworst=[]
    for i in range(0,m):
        tempb=0
        tempw=0
        for j in range(1,n):
            tempb+=pow(df.iloc[i,j]-vbest[j],2)
            tempw+=pow(df.iloc[i,j]-vworst[j],2)
        sbest.append(pow(tempb,0.5))
        sworst.append(pow(tempw,0.5))

    #Find performance score
    p=[]
    for i in range(0,m):
        p.append(sworst[i]/(sworst[i]+sbest[i]))

    df['Topsis Score']=p
    df['Rank']=df['Topsis Score'].rank(ascending=False)
    
    return df

#Main program starts here
def topsis(inputFile, weightsString, impactsString, outputFile):
    args=[None, inputFile, weightsString, impactsString, outputFile]
    
    if len(args) < 5:
        print("Wrong number of arguments!! Give 5 arguments atleast.")
        print("Example: python topsis.py <InputDataFileName> <Weights> <Impacts> <ResultFileName>")
        sys.exit()

    #Input the csv file
    try:
        datafile = args[1]
        if datafile[-4:]!=".csv" and datafile[-4:]!=".txt":
            print("Input file must be a .csv or .txt file!!")
            sys.exit()
        df = pd.read_csv(datafile)

    except: 
        #File not found
        print("File with given name does not exist!! Please check the file name and try again.")
        sys.exit()

    outfile = args[4]
    if outfile[-4:]!=".csv" and outfile[-4:]!=".txt":
        print("Output file file must be a .csv or .txt file!!")
        sys.exit()

    #Checking file has atleast three columns
    if df.shape[1]-1 < 3:
        print("Input file must have 3 columns atleast!!")
        sys.exit()

    #Check the type of columns 2 to end is numeric only
    for i in range(1,df.shape[1]):
        if not np.issubdtype(df.iloc[:,i],np.number):
            print("Column",i+1,"must contain numeric values only!!")
            sys.exit()

    #Obtaining the weights array
    try:
        weights = list(args[2].split(","))

    except:
        #Check if weights were incorrectly entered
        print("Enter valid weights separated by commas!!")
        sys.exit()

    if len(weights) != df.shape[1]-1:
        #Check if weights are not equal to the number of columns
        print("Weights must be equal to the number of features!!")
        sys.exit()

    #Obtaining the impacts array:
    try:
        impacts = list(args[3].split(","))

    except:
        #Check if impacts were incorrectly entered
        print("Enter valid impacts separated by commas!!")
        sys.exit()

    #Check if impacts are not equal to the number of columns
    if len(impacts) != df.shape[1]-1:
        print("Impacts must be equal to the number of features!!")
        sys.exit()

    #Check if given impacts are other than '+' or '-'
    for i in range(0,len(impacts)):
        if impacts[i] not in ('+','-'):
            print("Incorrect impact given. It must be '+' or '-' only!!")
            sys.exit()

    df_output=calcTopsis(df,weights,impacts)
    df_output.to_csv(outfile)

    print("TOPSIS is implemented successfully over the given input data!!")
    print("Output file is successfully saved at given path.")