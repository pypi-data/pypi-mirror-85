import numpy as np
import pandas as pd


def split(df, test_ratio=0.3):
    df['split'] = np.random.randn(df.shape[0], 1)
    msk = np.random.rand(len(df)) <= test_ratio
    test = df[msk]
    train = df[~msk]
    train.drop("split", axis=1, inplace=True)
    test.drop("split", axis=1, inplace=True)
    return train, test
