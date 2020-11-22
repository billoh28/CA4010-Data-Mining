import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics, tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from ufc_model import sanitation
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sn
from sklearn.ensemble import RandomForestClassifier

# Taking args off command line
# First argument for level of snaitition
# Second for which classifier
import sys

args = sys.argv[1:]

if int(args[1]) == 1:
    fight_dataset = sanitation(int(args[0]), True)

else:
    fight_dataset = sanitation(int(args[0]))

le = LabelEncoder()

fight_dataset = fight_dataset.apply(le.fit_transform)

print(fight_dataset.iloc[1, :-1])

X = fight_dataset.iloc[:, :-1].values
y = fight_dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = X[int(len(X) * .2):] , X[:int(len(X) * .2)], y[int(len(y) * .2):] , y[:int(len(y) * .2)]

#print(X_test[0])

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Random state 
classifier = RandomForestClassifier(max_depth=5, random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

df_cm = confusion_matrix(y_test, y_pred)
print(classification_report(y_test, y_pred))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

plt.figure(figsize = (10,7))

graph = sn.heatmap(df_cm, annot=True)
graph.set(xlabel='Predicted Label', ylabel='True Label')
plt.show()

#print(classifier.apply(X[:4]))