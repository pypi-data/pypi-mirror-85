# DIVYAM JAIN 101803128

# python topsis.py topsis_data.csv "1,1,1,2" "+,+,-,+" result.csv

import numpy as np
import pandas as pd
import os
import sys

rssRow = []


def rss(val):
    s = 0
    for x in val:
        s += np.square(x)
    s = np.sqrt(s)
    rssRow.append(s)


ideal_best = []
ideal_worst = []


best_dist = []
worst_dist = []


def euclidean_distance(val):

    s_plus = 0
    s_minus = 0
    for x, y, z in zip(list(val), ideal_best, ideal_worst):
        s_plus += np.square(x-y)
        s_minus += np.square(x-z)
    s_plus = np.sqrt(s_plus)
    s_minus = np.sqrt(s_minus)
    best_dist.append(s_plus)
    worst_dist.append(s_minus)


def CalculateTopsisScore(file, weight, impact):
    outputName = ".".join(file.split(".")[:-1])
    impact = [x.strip() for x in impact.split(",")]
    weight = [x.strip() for x in weight.split(",")]

    df = pd.read_csv(file)
    df_original = pd.read_csv(file)
    print("\nOriginal Data\n")
    print(df.head())
    for i, w in enumerate(weight):
        try:
            weight[i] = float(w)
            continue
        except ValueError:

            if not w.isnumeric():
                print(w)
                print("Weights of wrong fromat.")
                sys.exit()
            else:
                weight[i] = int(w)
    for i in impact:
        if i not in ["+", "-"]:
            print("Imapacts of wrong fromat.")
            sys.exit()

    # fread = open(file, "r")
    df = pd.read_csv(file)

    if file not in os.listdir():
        print("File {} not found.".format(file))
        sys.exit()
    elif len(df.columns[1:]) != len(weight):
        print("No. Of weights on not equal to data size !")
        sys.exit()
    elif len(df.columns[1:]) != len(impact):
        print("No. Of imapacts on not equal to data size !")
        # fread.close()
        sys.exit()
    elif len(df.columns[1:]) < 3:
        print("Input File must have More than 3 columns !")
        # fread.close()
        sys.exit()

    for a in list(df.iloc[:, 1:].dtypes):
        if a not in["float64", "int64"]:
            print("\nNon-Numeric data in csv file !")
            sys.exit()

    df.iloc[:, 1:].apply(func=rss, axis=0)

    for ind, val in enumerate(df.iloc[:, 1:].columns):
        df[val] = (df[val] / rssRow[ind]) * weight[ind]

    for ind, val in enumerate(df.iloc[:, 1:].columns):
        if impact[ind] == "+":
            ideal_best.append(df[val].max())
            ideal_worst.append(df[val].min())
        if impact[ind] == "-":
            ideal_best.append(df[val].min())
            ideal_worst.append(df[val].max())

    df.iloc[:, 1:].apply(func=euclidean_distance, axis=1)

    sum_dist = [x+y for x, y in zip(best_dist, worst_dist)]
    performance = [x/y for x, y in zip(worst_dist, sum_dist)]

    best_dist_df = pd.DataFrame(
        performance, columns=["Topsis Score"])

    df_original = pd.concat([df_original, best_dist_df], axis=1)

    df_original['Rank'] = df_original['Topsis Score'].rank(ascending=0)

    print("\nFinal Data\n")
    print(df_original.head())

    print("\n\nOutput Saved as {}-Output.csv\n".format(outputName))
    df_original.to_csv("{}-Output.csv".format(outputName))