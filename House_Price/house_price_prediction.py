# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 12:13:55 2017

@author: krish
"""

import numpy as np
import pandas as pd
train_source = pd.read_csv('train.csv')
desc = train_source.describe()
num_cols = list(desc.columns)
all_cols = list(train_source.columns)
cat_cols = [i for i in all_cols if i not in num_cols]
train_raw = train_source.copy(deep=True)
def data_preprocess(data, num_cols, cat_cols):
    for c in cat_cols:
        data.loc[data[c].isnull(),c]='Not Specified'
        data[c]=data[c].astype('category')
        data[c]=data[c].cat.codes
    for n in num_cols:
        data.loc[data[c].isnull(),c]=np.mean(data[c])
    return data


train = data_preprocess(train_raw, num_cols = num_cols, cat_cols=cat_cols)