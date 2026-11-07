import pandas as pd 
import numpy as np
from sklearn import datasets




def neigbors (X_test, X_train , y_pred , y_train,y_test,num_of_neighbour = 5):
    total_accuracy = 0
    y_pred_1 = pd.Series.copy(y_pred)
    for idx , row in X_test.iterrows():
        delta = X_train - row
        delta_square = delta.pow(2)
        delta_sum = delta_square.sum(axis = 1 , numeric_only = True)
        sort_delta  = delta_sum.sort_values (ascending = True)
        sort_delta_5 = sort_delta.iloc[:num_of_neighbour]
        indx = sort_delta_5.index
        val_y = y_train.loc[indx]
        moda = pd.Series.mode(val_y)
        y_pred_1.loc[idx] = moda.iloc[0]
        if y_pred_1.loc[idx] == y_test.loc[idx]:
            total_accuracy+= 1 / (y_test.shape[0]) * 100 
    return total_accuracy , y_pred_1




iris = datasets.load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.head()
df = df.sample(frac=1, random_state= 2007).reset_index(drop=True)
size = df.shape
total_accuracy = 0
print(size)
lines_num = size[0]
X_train = df.iloc[0:int(lines_num * 0.8) ].drop(columns = ['target'])
X_test = df.iloc[int(lines_num * 0.8) :].drop(columns = ['target'])
y_test = df.iloc[int(lines_num * 0.8) : , -1]
y_pred = pd.Series.copy(y_test, deep= True)
y_train = df.iloc[0:int(lines_num * 0.8)  , -1]

total_accuracy_copy = 0
X_copy_train = df.iloc[0:int(lines_num * 0.2)].drop(columns = ['target'])
X_copy_test = df.iloc[int(lines_num * 0.2) : ].drop(columns = ['target'])
y_copy_test = df.iloc[int(lines_num * 0.2) : , -1]
y_copy_pred = pd.Series.copy(y_copy_test, deep= True)
y_copy_train = df.iloc[0:int(lines_num * 0.2)  , -1]


acc1 , y_pred1 = neigbors(X_test ,X_train, y_pred , y_train , y_test)
acc2 , y_pred2= neigbors(X_copy_test , X_copy_train,y_copy_pred ,y_copy_train, y_copy_test  )
print (acc1 , y_pred1)
print(acc2 , y_pred2)



