import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics, tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from ufc_model import sanitation
from sklearn.metrics import classification_report, confusion_matrix

# Taking args off command line
# First argument for level of snaitition
# Second for which classifier
import sys

args = sys.argv[1:]

if int(args[1]) == 1:
    fight_dataset = sanitation(int(args[0]), True)

else:
    fight_dataset = sanitation(int(args[0]))

col = fight_dataset.columns # Save colums

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
classifier = DecisionTreeClassifier(random_state=21, max_depth = 5)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

df_cm = confusion_matrix(y_test, y_pred)
print(classification_report(y_test, y_pred))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

plt.figure(figsize = (10,7))

graph = sn.heatmap(df_cm, annot=True)
graph.set(xlabel='Predicted Label', ylabel='True Label')
plt.show()


# Print what every index of X is in order to see what the tree is splitting on
for i in range(len(col)):
     print("X[{:}] is: {:}".format(i, col[i]))


# # Plot tree
fig, ax = plt.subplots(figsize=(7,7))
plot_tree(classifier, max_depth=4, fontsize=6, filled=True)
plt.show()