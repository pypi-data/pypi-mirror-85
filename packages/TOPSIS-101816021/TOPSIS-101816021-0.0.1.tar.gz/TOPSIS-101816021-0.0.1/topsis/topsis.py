#IMPORTING ESSENTIAL LIBRARIES
from tabulate import tabulate
from os import path
import pandas as pd
import math as m
import sys

def topsis(filename, weights, impacts, resultFileName):
    # LOADING DATASET
    dataset = pd.read_csv(filename)

    # DROPPING EMPTY CELLS IF ANY
    dataset.dropna(inplace = True)

    # ONLY TAKING NUMERICAL VALUES
    d = dataset.iloc[0:,1:].values

    # CONVERTING INTO MATRIX
    matrix = pd.DataFrame(d)

    # CALCULATING SUM OF SQUARES
    sumOfSquares = []
    for col in range(0, len(matrix.columns)):
        X = matrix.iloc[0:,[col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sumOfSquares.append(m.sqrt(sum))
    # print(sumOfSquares)

    # DIVIDING ALL THE VALUES BY SUM OF SQUARES
    j = 0
    while(j < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[j][i] = matrix[j][i]/sumOfSquares[j] 
        j = j+1

    # MULTIPLYING BY WEIGHTS
    # weights = [0.25, 0.25, 0.25, 0.25]
    k = 0
    while(k < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[k][i] = matrix[k][i]*weights[k] 
        k = k+1

    # CALCULATING IDEAL BEST AND IDEAL WORST
    # impacts = ['+', '+', '-', '+']
    bestValue = []
    worstValue = []

    for col in range(0, len(matrix.columns)):
        Y = matrix.iloc[0:,[col]].values
        
        if impacts[col] == "+" :
            # print("+")
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(maxValue[0])
            worstValue.append(minValue[0])

        if impacts[col] == "-" :
            # print("-")
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(minValue[0])
            worstValue.append(maxValue[0])

    # CALCULATING Si+ & Si-
    SiPlus = []
    SiMinus = []

    for row in range(0, len(matrix)):
        temp = 0
        temp2 = 0
        wholeRow = matrix.iloc[row, 0:].values
        for value in range(0, len(wholeRow)):
            temp = temp + (m.pow(wholeRow[value] - bestValue[value], 2))
            temp2 = temp2 + (m.pow(wholeRow[value] - worstValue[value], 2))
        SiPlus.append(m.sqrt(temp))
        SiMinus.append(m.sqrt(temp2))

    # CALCULATING PERFORMANCE SCORE Pi
    Pi = []

    for row in range(0, len(matrix)):
        Pi.append(SiMinus[row]/(SiPlus[row] + SiMinus[row]))

    # CALCULATING RANK
    Rank = []
    sortedPi = sorted(Pi, reverse = True)

    for row in range(0, len(matrix)):
        for i in range(0, len(sortedPi)):
            if Pi[row] == sortedPi[i]:
                Rank.append(i+1)

    # INSERTING THE NEWLY CALCULATED COLUMNS INTO THE MATRIX
    col1 = dataset.iloc[:,[0]].values
    matrix.insert(0, dataset.columns[0], col1)
    matrix['Topsis Score'] = Pi
    matrix['Rank'] = Rank

    # RENAMING ALL THE COLUMNS
    newColNames = []
    for name in dataset.columns:
        newColNames.append(name)
    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    matrix.columns = newColNames

    # SAVING THE MATRIX INTO A CSV FILE
    matrix.to_csv(resultFileName)

    # PRINTING TO THE CONSOLE USING TABULATE PACKAGE
    print(tabulate(matrix, headers = matrix.columns))

def checkRequirements() :
    if len(sys.argv) == 5 :
        # filename
        filename = sys.argv[1].lower()
        # weights
        weights = sys.argv[2].split(",")
        for i in range(0, len(weights)):
            weights[i] = int(weights[i])
        # impacts
        impacts = sys.argv[3].split(",")
        # resultFileName
        resultFileName = sys.argv[-1].lower()
        if ".csv" not in resultFileName:
            print("RESULT FILENAME SHOULD CONTAIN '.csv'")
            return
        if path.exists(filename) :
            if len(weights) == len(impacts) :
                topsis(filename, weights, impacts, resultFileName)
            else :
                print("INPUT ERROR, NUMBER OF WEIGHTS AND IMPACTS SHOULD BE EQUAL")
                return
        else :
            print("INPUT FILE DOES NOT EXISTS ! CHECK YOUR INPUT")
            return
    else :
        print("REQUIRED NUMBER OF ARGUMENTS ARE'NT PROVIDED !")
        print("SAMPLE INPUT : python <script_name> <input_data_file_name> <weights> <impacts> <result_file_name>")
        return

# MAIN FUNCTION
# if everything is fine, it will call the topsis() function,
# otherwise will display appropriate error
checkRequirements()