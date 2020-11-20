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

# Get number of landed strikes total
fight_data["R_SIG_STR_NUM"] = fight_data["R_SIG_STR."].apply(lambda x: int(x.split()[0]) if type(x) == str else x)
fight_data["B_SIG_STR_NUM"] = fight_data["B_SIG_STR."].apply(lambda x: int(x.split()[0]) if type(x) == str else x)


# Change R_SIG_STR and B_SIG_STR from x of y to a float or integer percentage
fight_data["R_SIG_STR."] = fight_data["R_SIG_STR."].apply(lambda x: get_percentage(int(x.split()[0]), int(x.split()[-1])) if type(x) == str else x)
fight_data["B_SIG_STR."] = fight_data["B_SIG_STR."].apply(lambda x: get_percentage(int(x.split()[0]), int(x.split()[-1])) if type(x) == str else x)

# Boxplot
#boxplot = fight_data.boxplot(column=["R_SIG_STR.", "B_SIG_STR."], by="Categorical_Winner")
#plt.show()

# Now try plot all winners / losers against significant strikes
fight_data["Winners_Sig_Str_Per"] = fight_data.apply(lambda row: row["R_SIG_STR."] if row["Winner"] == 0 else row["B_SIG_STR."], axis=1)
fight_data["Losers_Sig_Str_Per"] = fight_data.apply(lambda row: row["B_SIG_STR."] if row["Winner"] == 0 else row["R_SIG_STR."], axis=1)

# Knockdowns
fight_data["Winners_KD_Per"] = fight_data.apply(lambda row: get_percentage(int(row["R_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))) if row["Winner"] == 0 else get_percentage(int(row["B_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))), axis=1)
fight_data["Losers_KD_Per"] = fight_data.apply(lambda row: get_percentage(int(row["R_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))) if row["Winner"] == 1 else get_percentage(int(row["B_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))), axis=1)

# Takedowns
#fight_data["Winners_TD_Per"] = fight_data.apply(lambda row: get_percentage(int(row["R_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))) if row["Winner"] == 0 else get_percentage(int(row["B_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))), axis=1)
#fight_data["Losers_TD_Per"] = fight_data.apply(lambda row: get_percentage(int(row["R_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))) if row["Winner"] == 1 else get_percentage(int(row["B_KD"]), (int(row["R_KD"]) + int(row["B_KD"]))), axis=1)

# Get percentage of all landed strikes for both fighters
#fight_data["Winners_Per_Total_Landed_Strikes"] = fight_data.apply(lambda row: get_percentage(row["R_SIG_STR_NUM"], (row["R_SIG_STR_NUM"] + row["B_SIG_STR_NUM"])) if row["Winner"] == 0 else get_percentage(row["B_SIG_STR_NUM"], (row["R_SIG_STR_NUM"] + row["B_SIG_STR_NUM"])), axis=1)
#fight_data["Losers_Per_Total_Landed_Strikes"] = fight_data.apply(lambda row: get_percentage(row["R_SIG_STR_NUM"], (row["R_SIG_STR_NUM"] + row["B_SIG_STR_NUM"])) if row["Winner"] == 1 else get_percentage(row["B_SIG_STR_NUM"], (row["R_SIG_STR_NUM"] + row["B_SIG_STR_NUM"])), axis=1)

# Tree splits on R_GROUND_landed so display results
fight_data["Winners_Landed_Ground_Attacks"] = fight_data.apply(lambda row: int(row["R_GROUND"].split()[0]) if row["Winner"] == 0 else int(row["B_GROUND"].split()[0]), axis=1)
fight_data["Losers_Landed_Ground_Attacks"] = fight_data.apply(lambda row: int(row["R_GROUND"].split()[0]) if row["Winner"] == 1 else int(row["B_GROUND"].split()[0]), axis=1)

# Now plot this
boxplot = fight_data.boxplot(column=["Winners_Landed_Ground_Attacks", "Losers_Landed_Ground_Attacks"])
plt.show()

print(fight_data["R_GROUND"].iloc[3])
