""" Lab 10: Save people
You can save people from heart disease by training a model to predict whether a person has heart disease or not.
The dataset is available at src/lab8/heart.csv
Train a model to predict whether a person has heart disease or not and test its performance.
You can usually improve the model by normalizing the input data. Try that and see if it improves the performance. 
"""
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np


data = pd.read_csv("src/lab10/heart.csv")

# Transform the categorical variables into dummy variables.
print(data.head())
string_col = data.select_dtypes(include="object").columns
df = pd.get_dummies(data, columns=string_col, drop_first=False)
print(data.head())

y = df.HeartDisease.values
x = df.drop(["HeartDisease"], axis=1)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=25
)

""" Train a sklearn model here. """

sklearn_model = KNeighborsClassifier(n_neighbors= 8)
sklearn_model.fit(x_train, y_train)


# Accuracy
print("Accuracy of model: {}\n".format(sklearn_model.score(x_test, y_test)))


df_max_scaled = df.copy()
for column in df_max_scaled.columns:
    df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()

y = df_max_scaled.HeartDisease.values
x = df_max_scaled.drop(["HeartDisease"], axis=1)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=25
)

sklearn_model = KNeighborsClassifier(n_neighbors= 8)
sklearn_model.fit(x_train, y_train)


""" Improve the model by normalizing the input data. """

print("Accuracy of improved model: {}\n".format(sklearn_model.score(x_test, y_test)))
