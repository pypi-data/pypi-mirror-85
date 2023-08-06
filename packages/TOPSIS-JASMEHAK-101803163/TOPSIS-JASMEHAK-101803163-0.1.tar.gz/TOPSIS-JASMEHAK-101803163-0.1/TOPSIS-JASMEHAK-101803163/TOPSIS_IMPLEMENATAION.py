import sys
import os
import pandas as pd
import numpy as np


def convert_sign(n):
    return int(n)

#vector normalization
def normalized(matrix, r, n, m):
    for j in range(m):
        sq = np.sqrt(sum(matrix[:, j] ** 2))
        for i in range(n):
            r[i, j] = matrix[i, j] / sq
    return r

#weighted normalized decision matrix
def weighted_product(matrix, weight):
    r = matrix * weight
    return r

#Calculate ideal best value and ideal worst value based on Impacts
def calc_ideal_vals(sign, matrix, n, m):
    ideal_worst = []
    ideal_best = []
    for i in range(m):
        if sign[i] == 1:
            ideal_worst.append(min(matrix[:, i]))
            ideal_best.append(max(matrix[:, i]))
        else:
            ideal_worst.append(max(matrix[:, i]))
            ideal_best.append(min(matrix[:, i]))
    return (ideal_worst, ideal_best)

#Calculate Euclidean distance from ideal best value and ideal worst value
def euclid_dist(matrix, ideal_worst, ideal_best, n, m):
    diw = (matrix - ideal_worst) ** 2
    dib = (matrix - ideal_best) ** 2
    dw = []
    db = []
    for i in range(n):
        dw.append(sum(diw[i, :]) ** 0.5)
        db.append(sum(dib[i, :]) ** 0.5)
    dw = np.array(dw)
    db = np.array(db)
    return (dw, db)


def performance_score(distance_worst, distance_best, n, m):
    score = []
    score = distance_worst / (distance_best + distance_worst)
    return score

#ranks based mon preformance score to find final result
def rankify(A):
    # Rank Vector
    R = [0 for x in range(len(A))]
    for i in range(len(A)):
        (r, s) = (1, 1)
        for j in range(len(A)):
            if j != i and A[j] > A[i]:
                r += 1
            if j != i and A[j] == A[i]:
                s += 1

        #obtain rank
        R[i] = r + (s - 1) / 2
        
    return R


def topsis():
    #check for no. of command line arguments
    if len(sys.argv) != 5:
        print('Incorrect no. of arguments.please try again')
        sys.exit()
    else:
        file_name = sys.argv[1]
        output_file = sys.argv[4]
        try:
            # check for file path
            if os.path.exists(file_name):
                pass
        except OSError as err:
            print(err.reason)
            exit(1)

        df= pd.read_csv(file_name)
        # This checks for correct no. of  columns in a file 
        if len(df.columns) < 3:  
            print('Not right number of columns in file')
            exit(0)

        a = df.values
        arg2 = sys.argv[2]  # "1,1,1,2"
        weight = arg2.split(',')
        #convert weights to float
        weight = list(map(float, weight))

        arg3 = sys.argv[3]  # "+,+,-,+"
        arg3 = arg3.replace('+', '1')
        arg3 = arg3.replace('-', '-1')
        impacts= arg3.split(',')
        #convert impacts to int
        sign = list(map(convert_sign, impacts))
        imp = [1, -1]
        for i in sign:
            # checks that impacts are + or - only
            if (i not in imp):
                print('impacts must be "+" or "-"')
                exit(0)
        # checks the len of impacts and weights
        if (len(impacts) != len(weight)):
            print('no. of weights not equal to no. of impacts')
            exit(0)
        a = df.drop(['Model'], axis=1).values

        row= len(a)
        cols= len(a[0])
        if (len(impacts) != cols):
            print('no. of weights and no. of impacts are not equal to no.of columns')
            exit(0)
        l = df._get_numeric_data()
        #checks if numeric data is present in cols or not
        if (len(l.columns)) != cols:
            print('non numeric data present in a column')
            exit(0)

        matrix= np.empty((row,cols), np.float64)
        matrix= normalized(a, matrix, row,cols)
        matrix_weighted= weighted_product(matrix, weight)
        (iWorstVal,iBestVal) = calc_ideal_vals(sign, matrix_weighted, row, cols)
        
        (euclid_worst,euclid_best) = euclid_dist(matrix_weighted, iWorstVal,iBestVal, row,cols)
        score = performance_score(euclid_worst,euclid_best, row, cols)
        rank = rankify(score)
        rank = list(map(int, rank))
        final_df =df
        final_df['Topsis Score'] = score
        final_df['Rank'] = rank
        final_df.to_csv(output_file, index=False)


if __name__ == '__main__':
    topsis()




