import sys
import pandas as pd

def function(infile,wt,im,outfile):
    try:
        df = pd.read_csv(infile)
        if len(df.columns) < 3:
            raise Exception('File must contain atleast three columns!')
        df1 = df.copy()
        weights = wt.split(',')
        impacts = im.split(',')
        if len(weights) != (len(df.columns) - 1) or len(impacts) != (len(df.columns) - 1):
            raise Exception('Number of weights,impacts and columns are not same!')

        def find_rss(col):
            s = 0
            for x in col:
                s = s + x ** 2
            rss = s ** (1 / 2)
            return rss

        for col in range(1, len(df.columns)):
            rss = find_rss(df.iloc[:, col])
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: x / rss)
        for i in range(0, len(weights)):
            weights[i] = float(weights[i])
        for col in range(1, len(df.columns)):
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: x * weights[col - 1])
        l1 = ['V+']
        l2 = ['V-']
        for col in range(1, len(df.columns)):
            if impacts[col - 1] == '+':
                l1.append(df.iloc[:, col].max())
                l2.append(df.iloc[:, col].min())
            else:
                l1.append(df.iloc[:, col].min())
                l2.append(df.iloc[:, col].max())
        df = df.append(pd.Series(l1, index=df.columns), ignore_index=True)
        df = df.append(pd.Series(l2, index=df.columns), ignore_index=True)
        l1 = []
        l2 = []
        rows = df.shape[0]
        for row in range(0, rows - 2):
            s1, s2 = 0, 0
            for col in range(1, len(df.columns)):
                s1 = s1 + (df.iloc[row, col] - df.iloc[rows - 2, col]) ** 2
                s2 = s2 + (df.iloc[row, col] - df.iloc[rows - 1, col]) ** 2
            l1.append(s1 ** (1 / 2))
            l2.append(s2 ** (1 / 2))
        df.drop([rows - 1, rows - 2], inplace=True)
        df['S+'] = l1
        df['S-'] = l2
        df['S+ + S-'] = df['S+'] + df['S-']
        df1['Topsis Score'] = df['S-'] / df['S+ + S-']
        df1['Rank'] = df1['Topsis Score'].rank(ascending=False)
        df1.to_csv(outfile, index=False)
    except FileNotFoundError:
        print('No File Found!')