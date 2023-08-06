import pandas as pd
import math
import time

def topsis(daf,weights,impacts):

    v_plus = []
    v_minus = []
    performance = []
    s_plus = []
    s_minus = []
    df = pd.DataFrame(daf)

    for i in range(0,len(df.columns)):
        df[df.columns[i]] = pd.to_numeric(df[df.columns[i]])
        series = df[df.columns[i]].apply(lambda x: x**2)
        series_sum = sum(series)
        series_root = math.sqrt(series_sum)

        df[df.columns[i]] = df[df.columns[i]].apply(lambda x: x / series_root)

        df[df.columns[i]] = df[df.columns[i]].apply(lambda x: x * weights[i])

        if impacts[i] == "+":
            v_plus.append(df[df.columns[i]].max())
            v_minus.append(df[df.columns[i]].min())

        else:
            v_plus.append(df[df.columns[i]].min())
            v_minus.append(df[df.columns[i]].max())

    for ind in df.index:
        pos = []
        neg = []
        for k in range(0,len(df.columns)):
            s_pos = df[df.columns[k]][ind] - v_plus[k]
            s_pos_squared = s_pos**2
            pos.append(s_pos_squared)
            s_neg = df[df.columns[k]][ind] - v_minus[k]
            s_neg_squared = s_neg**2
            neg.append(s_neg_squared)

        pos_squared_sum = sum(pos)
        pos_squared_root = math.sqrt(pos_squared_sum)
        s_plus.append(pos_squared_root)

        neg_squared_sum = sum(neg)
        neg_squared_root = math.sqrt(neg_squared_sum)
        s_minus.append(neg_squared_root)

    for s in range(0,len(s_plus)):
        p = s_minus[s]/(s_plus[s]+s_minus[s])
        performance.append(p)


    df_result = pd.DataFrame(performance,columns=['performance'])
    df_result['Rank'] = df_result['performance'].rank(ascending=False)
    df_result.to_csv('result' + str(time.time()) + '.csv', header=True)



