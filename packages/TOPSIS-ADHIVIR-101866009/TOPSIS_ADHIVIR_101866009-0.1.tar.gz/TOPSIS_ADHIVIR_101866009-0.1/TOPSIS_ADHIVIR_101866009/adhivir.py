import pandas as pd
import sys
# Author:- Adhivir Singh Rana 101866009 3CS3
def TOPSIS1():
    # Checking correct number of Parameters
    if (len(sys.argv) != 5):
        raise Exception('Incorrect number of parameters')

    # File Not found error
    try:
        data = pd.read_csv(sys.argv[1])
    except FileNotFoundError:
        print('File Not found!!')
        exit()
    rows = data.shape[0]
    columns = data.shape[1]

    # Handling of non numeric Characters from Column 2 to Last Column
    for i in range(0, rows):
        for j in range(1, columns):
            try:
                data.iloc[i, j] = float(data.iloc[i, j])
            except:
                raise Exception('Non-Numeric Entries Present')

    # Weight must be seperated by comma
    wts = []
    for i in range(0, len(sys.argv[2])):
        if (i % 2 == 1):
            if (sys.argv[2][i] != ','):
                raise Exception('Weights must be seperated by comma')
        else:
            try:
                wts = wts + [float(sys.argv[2][i])]
            except:
                raise Exception('Weights can be of type float or int only.')

    # Impacts must be either +ive or -ive
    imp = []
    for i in range(0, len(sys.argv[3])):
        if (i % 2 == 1):
            if (sys.argv[3][i] != ','):
                raise Exception('Input of Criteria must be seperated by comma')
        else:
            if (sys.argv[3][i] == '+' or sys.argv[3][i] == '-'):
                imp = imp + [sys.argv[3][i]]
            else:
                raise Exception('Impacts can only be +ive or -ive')

    # Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.
    if ((len(wts) != len(imp)) or (len(wts) != columns - 1) or (len(imp) != columns - 1)):
        raise Exception('Number of weights, number of impacts and number of columns from 2nd to last must be same')

    # Calculation of root of sum of squares
    root_sum = []
    for i in range(1, columns):
        x = data.iloc[:, i]
        y = sum(x * x)
        root_sum = root_sum + [(y ** 0.5)]

        # Normalised_matrix
    i = 0
    n_matrix = pd.DataFrame(data.iloc[:, 0])
    for c in data.columns:
        if i != 0:
            n_matrix[c] = data.iloc[:, i] / root_sum[i - 1]
        i = i + 1

    # Weighted__matrix
    weighted_matrix = pd.DataFrame(n_matrix.iloc[:, 0])
    i = 0
    for c in n_matrix.columns:
        if i != 0:
            weighted_matrix[c] = n_matrix.iloc[:, i] * wts[i - 1]
        i = i + 1

    # Making the list of ideal best and ideal worst
    ideal_best = []
    ideal_worst = []
    for i in range(0, columns - 1):
        if (imp[i] == '+'):
            ideal_best = ideal_best + [max(weighted_matrix.iloc[:, i + 1])]
            ideal_worst = ideal_worst + [min(weighted_matrix.iloc[:, i + 1])]
        elif imp[i] == '-':
            ideal_best = ideal_best + [min(weighted_matrix.iloc[:, i + 1])]
            ideal_worst = ideal_worst + [max(weighted_matrix.iloc[:, i + 1])]

    # Euclidean Distance Calculation for ideal best and worst
    euclidean_distance_ideal_best = []
    euclidean_distance_ideal_worst = []
    for i in range(0, rows):
        x = 0
        y = 0
        for j in range(0, columns - 1):
            x = x + (weighted_matrix.iloc[i, j + 1] - ideal_best[j]) * (weighted_matrix.iloc[i, j + 1] - ideal_best[j])
            y = y + (weighted_matrix.iloc[i, j + 1] - ideal_worst[j]) * (
                        weighted_matrix.iloc[i, j + 1] - ideal_worst[j])
        euclidean_distance_ideal_best = euclidean_distance_ideal_best + [x ** 0.5]
        euclidean_distance_ideal_worst = euclidean_distance_ideal_worst + [y ** 0.5]

    # Sum of Euclidean distance of ideal best and ideal worst
    euclidean_distance_both = []
    for i in range(0, rows):
        euclidean_distance_both = euclidean_distance_both + [
            euclidean_distance_ideal_best[i] + euclidean_distance_ideal_worst[i]]

    # Calculating the TOPSIS score
    topsis_score = []
    for i in range(0, rows):
        topsis_score = topsis_score + [euclidean_distance_ideal_worst[i] / euclidean_distance_both[i]]

    # Calculating the rank
    rank = []
    for i in range(0, rows):
        count = 0
        for j in range(0, rows):
            if (i != j and topsis_score[i] < topsis_score[j]):
                count = count + 1
        rank = rank + [count + 1]

    # Storing the TOPSIS Score and Rank
    data['TOPSIS SCORE'] = topsis_score
    data['RANK'] = rank
    print("The desired result:\n")
    print(data)

    # Output File Creation
    data.to_csv(sys.argv[4], index=False)
    print("Calculations done and file created!!")


TOPSIS1()