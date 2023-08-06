import sys
import csv
import pandas as pd
import logging


def topsis(inputFileName,weights,impacts,resultFileName):

    try:
        df = pd.read_csv(inputFileName)
    except:
        logging.warning("File '" + inputFileName + "' not found")
        return

    try:
        weights = list(map(int, weights.split(',')))
    except ValueError:
        logging.warning("Please use commas to seperate weights. Weights: "+ weights)
        return

    try:
        impacts = list(impacts.split(','))
        for i in impacts:
            if i != '+' and i != '-':
                logging.warning("Impacts contain values other than '+' and '-'.\nImpacts: " + impacts)
                return
        if len(weights) != len(impacts):
            logging.warning("Number of weights and impacts are different.")
            return
        
        if len(df.columns) < 3:
            logging.warning("There is only one or less Models in input file.")
            return
        if (len(df.columns)-1) != len(weights):
            logging.warning("Number of weights and attributes are not the same.")
            return
        for idt in df.dtypes[1:]:
            if idt != "float64":
                logging.warning("Input file contains non numeric values.")
                return


    rootSquaredSum = []
    for i in df.columns[1:]:
        total = 0
        for j in list(df[i]):
            total += j**2
        rootSquaredSum.append(total**(0.5))
    for index,i in enumerate(df.columns[1:]):
        for j in df[i]:
            df[i] = df[i].replace(j,j*weights[index]/rootSquaredSum[index])


    ideal = []
    for index,i in enumerate(df.columns[1:]):
        if impacts[index] == '+':
            idealBest = max(df[i])
            idealWorst = min(df[i])
        else:
            idealBest = min(df[i])
            idealWorst = max(df[i])

        ideal.append((idealBest, idealWorst))

    n = len(df.index)
    D = []
    for i in range(n):
        totalPositive = 0
        totalNegative = 0
        for index,j in enumerate(list(df.iloc[i])[1:]):
            totalPositive += ((j-ideal[index][0])**2)
            totalNegative += ((j-ideal[index][1])**2)
      
        D.append(totalNegative/totalPositive+totalNegative)

    final = pd.read_csv(inputFileName)
    final["Topsis Score"] = D
    final["Rank"] = final["Topsis Score"].rank(ascending=False)
    for i in final["Rank"]:
        final["Rank"] = final["Rank"].replace(i,'{:0g}'.format(i))
    # print(final)

    final.to_csv(resultFileName,index=False)
    print("CSV file '" + resultFileName + "' has been created.")