import time
import numpy as np
import pandas as pd


def get_diff_from_initial_value(series):
    return (series / (series.iat[0] - 1))


def convert_datetimeindex_to_timestamp(index):
    return (index.astype(np.int64).astype(np.float) // 10**9) + time.timezone


def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop


def get_top_correlations(df, n=5):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]


def get_bottom_correlations(df, n=5):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]


def read_sql(sql, con):
    '''
    read_sql with chunk 1000 not to make a big transaction.
    '''
    chunks = []
    for chunk in pd.read_sql(sql, con, chunksize=1000):
        chunks.append(chunk)

    if len(chunks) > 0:
        return pd.concat(chunks, axis=0)
    else:
        return None


def show_all_columns():
    return pd.option_context('display.max_columns', 99999)


def show_all_rows():
    return pd.option_context('display.max_rows', 99999)


def show_all_dataframe():
    return pd.option_context('display.max_rows', 999999, 'display.max_columns', 999999)
