from sys import float_repr_style
import pandas as pd
import numpy as np
import sys
def topsis(arg1,arg2,arg3,arg4):
    try:
        dfd = pd.read_csv(f'{arg1}')
    except:
        print("File not Found ")
        sys.exit()
    df = dfd
    if len(df.columns) < 3:
        print("file must have more than 2 columns")
        sys.exit()
    for col in df.columns:
        if col != df.columns[0]:
            for row in range(len(df)):
                if type(df[col][row]) == 'numpy.float64':
                    print("non-numaric value in column ", col)
                    sys.exit()

    l = list()
    for col in df.columns:
        s = 0.00

        if col != df.columns[0]:
            for row in range(len(df)):
                s += float(df[col][row] ** 2)
            s = np.sqrt(s)
            l.append(s)
    try:
        w = arg2.split(",")
    except:
        print("weights must be seprated by comma")
        sys.exit()
    if len(w) != len(df.columns) - 1:
        print("wrong no of weights")
        sys.exit()

    count = 0
    for col in df.columns:
        if col != df.columns[0]:
            df[col] = df[col].div(l[count])
            m = float(w[count])
            df[col] = df[col] * m
            count += 1
    try:
        weight = arg3.split(",")
    except:
        print("Impacts must be seprated by comma")
        sys.exit()
    if len(weight) != len(df.columns) - 1:
        print("wrong no of impacts")
        sys.exit()

    vp = list()
    vm = list()
    count = 0
    for col in df.columns:
        if col != df.columns[0]:
            if weight[count] == '+':
                vp.append(max(df[col]))
                vm.append(min(df[col]))
            else:
                vm.append(max(df[col]))
                vp.append(min(df[col]))
            count += 1

    sp = list()
    sm = list()

    for row in range(len(df)):
        count = 0
        s1 = 0.00
        s2 = 0.00
        for col in df.columns:
            if col != df.columns[0]:
                s1 = s1 + float((df[col][row] - vp[count]) ** 2)
                s2 = s2 + float((df[col][row] - vm[count]) ** 2)
                count += 1
        sp.append(np.sqrt(s1))
        sm.append(np.sqrt(s2))

    p = list()
    for i in range(len(df)):
        p.append(sm[i] / (sp[i] + sm[i]))

    dfd['Topsis Score'] = p
    r = list()
    for i in range(len(df)):
        r.append(len(df) - i)

    dfd.sort_values(by='Topsis Score', inplace=True)
    dfd['Rank'] = r
    dfd['index'] = df.index
    dfd.sort_values(by='index', inplace=True)
    dfd.drop(columns='index', inplace=True)
    dfd.set_index(dfd.columns[0], inplace=True)

    nme1 = arg4
    dfd.to_csv(f'{nme1}')





