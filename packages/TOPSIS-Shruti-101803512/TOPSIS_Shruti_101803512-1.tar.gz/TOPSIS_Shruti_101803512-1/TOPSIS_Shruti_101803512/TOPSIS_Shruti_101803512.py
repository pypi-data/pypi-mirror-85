import pandas as pd
import sys
import math
import numpy as np


def main():
    if len(sys.argv) != 5:
        print("Error !! Wrong number of parameters")       # Checking if correct number of arguments are given
        print("Exactly five parameter are required")
        print("usages: python topsis.py <string1> <string2> <string3> <string4>")   # Error raised if incorrect
        print("example: python topsis.py <inputFileName> <Weights> <Impacts> <resultFileName>")
        exit(0)
    filename = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]
    topsis_evaluation(filename, weights, impacts, result_file)


def topsis_evaluation(filename, weights, impacts, result_file):
    weights = list(weights.split(","))
    impacts = list(impacts.split(","))
    try:
        f = open(filename, 'r')                     # Checking if the csv file of dataset given is present
    except FileNotFoundError:                          # If not Exception raised of FileNotFound
        print("The above csv file does not exist")   # Keep the python file and csv file in same folder
        exit(0)
    myData = pd.read_csv(filename, header=0, index_col=False)   # Reading data from csv file
    if not len(myData.columns) >= 3:  # Checking if input file contains three or more columns
        print(f"Error !! Wrong number of columns in {filename}")
        print("Equal to or greater than three columns are required")  # Exiting if not correct number of columns
        exit(0)
    cols = list(myData.columns)
    for i in list(range(1, len(cols))):   # Verifying if columns from 2nd column are only numeric values
        if myData[cols[i]].dtypes == object:
            print("From 2nd to last columns must contain numeric values only ")
            print("Please check your data file")
            exit()
    if len(cols) - 1 != len(weights):     # Verifying if number of weights and number of columns are same.
        print("Number of weights and number of columns (from 2nd to last columns) must be same.")
    if len(cols) - 1 != len(impacts):     # Verifying if number of impacts and number of columns are same.
        print("Number of impacts and number of columns (from 2nd to last columns) must be same.")
    for i in impacts:
        if i != '+' and i != '-':         # Verifying that impacts must be + or - only
            print("Impacts must be either +ve or -ve")
            print("Please check the impacts provided")
            break
    (rows, columns) = myData.shape         # Performing topsis
    myData1 = np.array(myData.iloc[:, 1:], dtype=np.float64)
    temp = []
    for i in range(0, columns-1):          # Vector normalization
        sqroot = 0
        for j in range(0, rows):
            sqroot = sqroot + pow(myData1[j, i], 2)
        sqroot = math.sqrt(sqroot)
        temp.append(sqroot)
    for i in range(0, columns-1):          # Weight Assignment
        for j in range(0, rows):
            myData1[j, i] = (myData1[j, i]/temp[i]) * float(weights[i])
    best = np.amax(myData1, axis=0)
    worst = np.amin(myData1, axis=0)       # Finding ideal best and ideal worst
    for i in range(len(impacts)):
        if impacts[i] == '+':
            pass
        elif impacts[i] == '-':
            t = worst[i]
            worst[i] = best[i]
            best[i] = t
    performance = []                       # Finding Euclidean distance
    for i in range(0, rows):
        s_p, s_n, p = 0, 0, 0
        for j in range(0, columns-1):
            s_p = s_p + pow((myData1[i][j] - best[j]), 2)
            s_n = s_n + pow((myData1[i][j] - worst[j]), 2)
        s_p = pow(s_p, 0.5)
        s_n = pow(s_n, 0.5)
        p = s_n / (s_p + s_n)              # Calculating performance score
        performance.append(p)
    s = sorted(performance, reverse=True)
    rank = []
    for i in performance:
        rank.append(s.index(i) + 1)        # Topsis score and rank
    myData['Topsis Score'] = performance   # Adding topsis score and rank to myData
    myData['Rank'] = rank
    myData.to_csv(result_file, index=False)   # Storing th results in csv file


if __name__ == "__main__":
    main()