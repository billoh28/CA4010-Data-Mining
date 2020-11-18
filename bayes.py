import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from ufc_model import sanitation
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

fight_dataset = sanitation(2)

le = LabelEncoder()

fight_dataset = fight_dataset.apply(le.fit_transform)

X = fight_dataset.iloc[:, :-1].values
y = fight_dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = X[int(len(X) * .2):] , X[:int(len(X) * .2)], y[int(len(y) * .2):] , y[:int(len(y) * .2)]

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

classifier = GaussianNB()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))