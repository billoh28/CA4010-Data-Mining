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


fight_dataset = sanitation(2)

le = LabelEncoder()

fight_dataset = fight_dataset.apply(le.fit_transform)

X = fight_dataset.iloc[:, :-1].values
y = fight_dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = X[int(len(X) * .2):] , X[:int(len(X) * .2)], y[int(len(y) * .2):] , y[:int(len(y) * .2)]

#print(X_test[0])

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Random state 
classifier = DecisionTreeClassifier(random_state=21)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Plot tree
fig, ax = plt.subplots(figsize=(15,12))
plot_tree(classifier, max_depth=8, fontsize=5, filled=True)
plt.show()