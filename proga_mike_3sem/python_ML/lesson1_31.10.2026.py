import pandas as pd 
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
print(lines_num)
print(df)
print(y_train)
print (X_train)
