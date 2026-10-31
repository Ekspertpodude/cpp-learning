import pandas as pd 
import numpy as np
from sklearn import datasets
iris = datasets.load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.head()
df = df.sample(frac=1).reset_index(drop=True)
size = df.shape
lines_num = size[0]
X_train = df.iloc[0:int(lines_num * 0.8) ].drop(columns = ['target'])
X_test = df.iloc[int(lines_num * 0.8) :].drop(columns = ['target'])
y_test = df.iloc[int(lines_num * 0.8) : , -1]
y_train = df.iloc[0:int(lines_num * 0.8)  , -1]

for idx , row in X_test.iterrows():
    delta = X_train - row
    delta_square = delta.pow(2)
    delta_sum = delta_square.sum(axis = 1 , numeric_only = True)
    sort_delta  = delta_sum.sort_values (ascending = True)
    sort_delta_5 = sort_delta.iloc[:5]
    print(sort_delta_5)

