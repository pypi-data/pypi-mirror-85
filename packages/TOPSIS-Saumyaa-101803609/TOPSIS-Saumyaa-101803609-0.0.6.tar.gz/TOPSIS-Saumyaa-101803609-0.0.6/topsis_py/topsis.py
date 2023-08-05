import pandas as pd
import math
import numbers
from statistics import mean
def topsis(file, weight, impact, outputfile):
    ''' 
    :param file (.csv): input csv file which contains 3 or more columns such that column 1 is the variable name,column 2 to n are numeric,
    :param weight (string): weight of each column
    :param impact (string): can be '+' or '-' where '+' means max is best and '-' means min is best
    :param outputfile (.csv): the result file containing the topsis score and rank of variables according to the score
    :return: 0 for success, -1 for failure
    Steps:  1)Calculate the root of sum of squares (RSS).
            2)Find Normalized Decision Matrix -Divide every column value its Root of Sum of Squares.
            3)Value in every cell is known as Normalized performance value.
            4)Calculate weight * normalized performance value.
            5)Calculate ideal best (ib) value and ideal worst value (iw).
            6)Calculate Euclidean distance from ideal best value (s0) and ideal worst value(s1).
            7)Calculate Performance Score (topsis score).
            8)Rank according to performance score ( Highest= Rank 1)
    '''
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print('File not found!!')
        return -1
    r, c = df.shape
    if c < 3:
        print("inappropriate no of columns")
        return -1
    df2 = df.iloc[:, 1:c].copy(deep=True)
    for ind, ele in df2.iterrows():
        for e in ele:
            if not isinstance(e, numbers.Number):
                print("non numeric data")
                return -1
    weights = weight
    if ',' not in weights:
        print("wrong separator")
        return -1
    weights = weights.strip("''")
    w = []
    w = weights.split(',')
    impacts = impact
    if ',' not in impacts:
        print("wrong separator")
        return -1
    impacts = impacts.strip("''")
    im = []
    im = impacts.split(',')
    if len(w) != len(im) or len(w) != c - 1:
        print("unequal weights or impacts or columns OR wrong separator")
        return -1
    try:
        w = [float(i) for i in w]
    except:
        print("non numeric weights")
        return -1
    for i in im:
        if i != '+' and i != '-':
            print("impact is neither +ve nor -ve")
            return -1
    df1 = df.copy(deep=True)
    ib = []
    iw = []
    for j in range(1, 5):
        sumx = 0
        r = 0
        for i in range(len(df)):
            sumx += math.pow(df.iloc[i, j], 2)
            r = math.pow(sumx, 0.5)
        df.iloc[:, j] /= r
        df.iloc[:, j] *= w[j - 1]
        if im[j - 1] == '+':
            ib.append(max(df.iloc[:, j]))
            iw.append(min(df.iloc[:, j]))
        else:
            ib.append(min(df.iloc[:, j]))
            iw.append(max(df.iloc[:, j]))
    l = [ib, iw]
    for ind in range(len(l)):
        df['s' + str(ind)] = ''
        for i in range(len(df)):
            d = 0
            sumx = 0
            for j in range(1, 5):
                diff1 = 0
                d1 = df.iloc[i, j]
                d2 = l[ind][j - 1]
                diff1 = d2 - d1
                sq = math.pow(diff1, 2)
                sumx += sq
            d = math.pow(sumx, 0.5)
            df.iloc[i, ind + 5] = d
    df['sum'] = df['s0'] + df['s1']
    df1['TOPSIS score'] = df['s1'] / df['sum']
    df1["Rank"] = df1['TOPSIS score'].rank(ascending=False)
    df1.to_csv(outputfile)
    return 0
