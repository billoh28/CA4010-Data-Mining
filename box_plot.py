import os
import numpy as np
import pandas as pd
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
fight_data["Categorical_Winner"] = fight_data.apply((lambda row: "Red" if extract_winner(row) == 0 else "Blue"), axis=1)
fight_data["Winner"] = fight_data.apply(lambda row: (extract_winner(row)), axis=1)

def get_percentage(x, y):
	try:
		return (x / y) * 100
	except:
		return 0

# Change R_SIG_STR and B_SIG_STR from x of y to a float or integer percentage
fight_data["R_SIG_STR."] = fight_data["R_SIG_STR."].apply(lambda x: get_percentage(int(x.split()[0]), int(x.split()[-1])) if type(x) == str else x)
fight_data["B_SIG_STR."] = fight_data["B_SIG_STR."].apply(lambda x: get_percentage(int(x.split()[0]), int(x.split()[-1])) if type(x) == str else x)

# Boxplot
#boxplot = fight_data.boxplot(column=["R_SIG_STR.", "B_SIG_STR."], by="Categorical_Winner")
#plt.show()

# Now try plot all winners / losers against significant strikes
fight_data["winners_sig_str_percentage"] = fight_data.apply(lambda row: row["R_SIG_STR."] if row["Winner"] == 0 else row["B_SIG_STR."], axis=1)
fight_data["losers_sig_str_percentage"] = fight_data.apply(lambda row: row["B_SIG_STR."] if row["Winner"] == 0 else row["R_SIG_STR."], axis=1)

# Now plot this
boxplot = fight_data.boxplot(column=["winners_sig_str_percentage", "losers_sig_str_percentage"])
plt.show()

print(fight_data.iloc[3])
