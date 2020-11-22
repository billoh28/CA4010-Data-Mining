import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def extract_winner(row):
    # Extract if red or blue won
    red = row["R_fighter"].lower()
    blue = row["B_fighter"].lower()
    winner = row["Winner"].lower()

    # No draws in dataset
    if winner == blue:
        return 1

    return 0

# This program will produce a box plot conveying winner loser strike attempted and landed percentages

# Load in fight data
fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_total_fight_data.csv"), sep=';')

# Remove nans
fight_data = fight_data.dropna(axis=0, how='any')

# Convert winners from their names into Red(0) or Blue(1)
fight_data["Winner"] = fight_data.apply(lambda row: (extract_winner(row)), axis=1)

values = fight_data["Winner"].value_counts()

labels = ["Red", "Blue"]

# Now plot this
hist = sns.barplot(x=labels,y=values)
plt.title('Histogram Showing Dispersion of Winners per Corner')
plt.ylabel('Number of Winners')
plt.show()

