import pandas as pd
import math
import sys
import os
import numpy as np


def save_topsis(loc_input,WEIGHTS,TARGET,loc_output):

    fileName,fileExtension = os.path.splitext(loc_input)
    fileName1,fileExtension1 = os.path.splitext(loc_output)

    if(fileExtension!='.csv'):
        raise Exception("Please enter a csv file as input...")
    if(fileExtension1!='.csv'):
        raise Exception("Please enter the output file as csv output...")
    weight = WEIGHTS
    weights = weight.split(',')
    targets = TARGET
    target = targets.split(',')

    if(len(weight)==len(weights)):
        raise Exception("Please separate the input weights with commas...")
    if(len(targets)==len(target)):
        raise Exception("Please separate the input targets with commas...")

    if(not os.path.exists(loc_input)):
        raise Exception("File is not existant...check path...")

    df = pd.read_csv(loc_input)
    data = df.values
    if(data.shape[1]<=2):
        raise Exception("Incorrect input file format ...atleast 3 columns required in input file...")

    if(df.isnull().values.any()):
        raise Exception("Some nan entry found in input file...")

    data = data[:,1:]

    if(len(weights)!=len(target)):
        raise Exception("Please check the size of weights and target...")

    if(data.shape[1]!=len(weights)):
        raise Exception("The entered input file and weights size does not match...")

    for i in range(len(target)):
        if(target[i]!='+' and target[i]!='-'):
            raise Exception("The entered target can contain only + and - signs...")

    ########### Normalising the data ################
    rows = data.shape[0]
    cols = data.shape[1]

    under_squares = []

    for i in range(cols):
        under_squares.append(round(math.sqrt(sum(data[:,i]**2)),2))

    for i in range(cols):
        for j in range(rows):
            data[j][i] = round(data[j][i]/under_squares[i],2)
    ########### Normalising the data ################

    ########### using weights ################
    for i in range(len(weights)):
        weights[i] = float(weights[i])

    for i in range(rows):
        for j in range(cols):
            data[i][j] = round(data[i][j]*weights[j],2)

    ########### using weights ################

    ########### finding ideals ################
    ideal_best = []
    ideal_worst = []

    for i in range(cols):
        if(target[i]=='+'):
            ideal_best.append(max(data[:,i]))
            ideal_worst.append(min(data[:,i]))
        else:
            ideal_best.append(min(data[:,i]))
            ideal_worst.append(max(data[:,i]))


    ########### finding ideals ################

    ########### euclidean dist ################
    euc_max = []
    euc_min = []

    for i in range(rows):
        temp = data[i,:]
        euc_max.append(round(math.sqrt(sum((temp-ideal_best)**2)),2))
        euc_min.append(round(math.sqrt(sum((temp-ideal_worst)**2)),2))
    ########### euclidean dist ################

    ########### topsis score ################
    topsis_score = []

    for i in range(rows):
        topsis_score.append(round((euc_min[i]/(euc_max[i]+euc_min[i])),2))

    ########### topsis score ################

    ########### rank ################
    rank = []

    def findrank(array,index):
        temp = array[index]
        rank = 1
        for i in range(len(array)):
            if(array[i]>temp):
                rank = rank + 1
        return rank

    for i in range(len(topsis_score)):
        rank.append(findrank(topsis_score,i))

    ########### rank ################

    ########### dataframes ################
    topsis = pd.DataFrame(topsis_score,columns=["Topsis Score"],index=None)
    ranks = pd.DataFrame(rank,columns=["Rank"],index=None)

    final_df = pd.concat([df,topsis,ranks],axis=1)

    final_df.to_csv(loc_output,index=False)
    print("Successfully saved the file where u wanted...")