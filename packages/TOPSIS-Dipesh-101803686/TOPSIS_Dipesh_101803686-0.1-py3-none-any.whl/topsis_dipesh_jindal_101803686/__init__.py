import pandas as pd
import sys
from os import path
import math

def calculate_Topsis_Score(inputFile, weight, impact, outputFile):
    dataset_name = inputFile
    if not path.exists(dataset_name):
        print('File not Found')
        return
    if not dataset_name.endswith('.csv'):
        print('choose csv file only')
        return

    dataset = pd.read_csv(dataset_name)

    if not len(dataset.columns) >= 3:
        print('Input file must contain three or more columns')
        return
    if dataset.iloc[:, 0].dtype != 'object':
        print('First column should be of object type')
        return
    for i in range(1, len(dataset.columns)):
        if dataset.iloc[:, i].dtype != 'float64' and dataset.iloc[:, i].dtype != 'int64':
            print('other columns should be of numeric type')
            return

    weights = weight.split(',')
    if len(weights) != len(dataset.columns) - 1:
        print('incorrect length of weights')
        return
    for numeric_string in weights:
        if not numeric_string.isnumeric():
            print('incorrect type of weights')
            return
    weights = [int(numeric_string) for numeric_string in weights]

    impacts = impact.split(',')
    if len(impacts) != len(dataset.columns) - 1:
        print('incorrect length of impacts')
        return
    for string in impacts:
        if string != '+' and string != '-':
            print("incorrect type of impacts")
            return

    if not outputFile.endswith('.csv'):
        print('output file should be csv only')
        return

    df = dataset.iloc[:, 1:]

    def calc(data, col_name):
        avg = 0
        for i in data[col_name]:
            avg += i ** 2
        avg = math.sqrt(avg)
        return avg

    avg_values = [calc(df, name) for name in df.columns]

    for i in df.columns:
        df[i] = df[i].apply(lambda x: x / avg_values[df.columns.get_loc(i)])
        df[i] = df[i].apply(lambda x: x * weights[df.columns.get_loc(i)])

    ideal_best = []
    ideal_worst = []

    for i in df.columns:
        if impacts[df.columns.get_loc(i)] == '-':
            ideal_best.append(min(df[i]))
            ideal_worst.append(max(df[i]))
        else:
            ideal_best.append(max(df[i]))
            ideal_worst.append(min(df[i]))

    dis_from_best = []
    dis_from_worst = []

    for i in range(len(df)):
        num = 0
        num2 = 0
        for j in df.columns:
            num += (df.loc[i, j] - ideal_best[df.columns.get_loc(j)]) ** 2
            num2 += (df.loc[i, j] - ideal_worst[df.columns.get_loc(j)]) ** 2
        num = math.sqrt(num)
        num2 = math.sqrt(num2)
        dis_from_best.append(num)
        dis_from_worst.append(num2)

    df['S+'] = dis_from_best
    df['S-'] = dis_from_worst

    dataset['Topsis Score'] = df['S-'] / (df['S+'] + df['S-'])
    dataset["Rank"] = dataset['Topsis Score'].rank(ascending=0)
    try:
        dataset.to_csv(outputFile, index=False)
    except Exception as e:
        print(e)