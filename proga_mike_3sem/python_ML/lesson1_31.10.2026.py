import pandas as pd 
from sklearn import datasets
iris = datasets.load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.head()
df = df.sample(frac=1).reset_index(drop=True)
size = df.shape
lines_num = size[1]
X_train = df.iloc[0: (lines_num //8) * 10 ]
X_test = df.iloc[(lines_num //8) * 10:]
print(df)