import string
import sys
import numpy as np
import pandas as pd

def topsis():
    if len(sys.argv) < 5:
        print("Incorrect Number Of Parameters")
        exit()

    fname = sys.argv[1]
    try:
        op = open(fname, 'r')
        op.close()
    except FileNotFoundError:
        print("File Not Found")
        exit()

    dframe = pd.read_csv(fname)
    if len(dframe.columns) < 4:
        print("Low No. Of Columns in File")
        exit()

    if len(dframe.select_dtypes(include=["float", "int"]).columns) + 1 != len(dframe.columns):
        print("Non-Numeric Values are present")
        exit()

    weight = sys.argv[2]
    impact = sys.argv[3]
    for i in string.punctuation:
        if i != ',':
            if i in weight:
                print("Use Commas")
                exit()
            if i != '+' and i != '-' and i in impact:
                print("Use Commas")
                exit()
    weight = weight.split(',')
    try:
        for i in range(len(weight)):
            weight[i] = int(weight[i])
    except ValueError:
        print("Weight sequence is wrong")
        exit()
    impact = impact.split(',')

    if len(weight) != len(impact) or len(weight) != len(dframe.columns) - 1 or len(impact) != len(dframe.columns) - 1:
        print("Unequal No. of Weights, Impact and Columns")
        exit()

    for i in impact:
        if i != '+' and i != '-':
            print("Impact sequence is wrong")
            exit()

    data = dframe.iloc[:, 1:].values
    row = len(data)
    column = len(data[0])
    s = sum(weight)

    if len(weight) != column:
        print("INSUFFICIENT WEIGHTS")
        sys.exit()

    for i in range(column):
        weight[i] /= s

    topsis_score = [0.0] * column

    for i in range(row):
        for j in range(column):
            topsis_score[j] = topsis_score[j] + (data[i][j] * data[i][j])

    for j in range(column):
        topsis_score[j] = pow(topsis_score[j], 0.5)

    for i in range(row):
        for j in range(column):
            data[i][j] /= topsis_score[j]
            data[i][j] *= weight[j]

    max_val = np.max(data, axis=0)
    min_val = np.min(data, axis=0)

    for i in range(column):
        if impact[i] == '-':
            max_val[i], min_val[i] = min_val[i], max_val[i]

    eucl_plus = []
    eucl_minus = []

    for i in range(row):
        splus = 0
        sminus = 0
        for j in range(column):
            splus += pow((data[i][j] - max_val[j]), 2)
            sminus += pow((data[i][j] - min_val[j]), 2)
        eucl_plus.append(float(pow(splus, 0.5)))
        eucl_minus.append(float(pow(sminus, 0.5)))

    topsis_score = []

    for i in range(row):
        topsis_score.append(eucl_minus[i] / (eucl_minus[i] + eucl_plus[i]))
    sort_form = sorted(topsis_score, reverse=True)

    rank = []
    for i in range(row):
        for j in range(row):
            if topsis_score[i] == sort_form[j]:
                rank.append(j + 1)

    dframe['Topsis'] = topsis_score
    dframe['Rank'] = rank
    dframe.to_csv(sys.argv[4], index=False)

def main():
    topsis()

if __name__ == "__main__":
    main()