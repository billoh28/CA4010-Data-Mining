# Want get the weights of NaN valued fighters
# To do this, gonna go through the g=fights dataset and get vthe weight class they fight in
# This is gonna be difficult of womans and mens fighters
# Data.csv has either "Womman's Whatever" or for mens just the weight class name
# Need to write two dictionarys to map weight class to weight for both men and women

import os
import numpy as np
import pandas as pd

def get_weight(fighter):
    # read in fight dataset
    fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "data.csv"), sep=',')

    # Run through this dataset and parse required info
    #print(fight_data["weight_class"].value_counts(dropna=False))

    weights = {"Strawweight":115, "Flyweight":125, "Bantamweight":135, "Featherweight":145, "Lightweight":155, "Welterweight":170, "Middleweight":185, "Light Heavyweight":205, "Heavyweight":265}

    # Go through data and find fighter
    for index, row in fight_data.iterrows():
        if str(row["R_fighter"]) == fighter or str(row["B_fighter"]) == fighter:
            if not pd.isna(row["weight_class"]) and (str(row["weight_class"]) in weights):
                return weights[str(row["weight_class"])]

            elif not pd.isna(row["weight_class"]) and (str(row["weight_class"].split()[-1]) in weights):
                return weights[str(row["weight_class"].split()[-1])]

    return None # If fighter not found or catch / open weight


def main():
    fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))

    print(fighter_detail["Weight"].value_counts())
    print(fighter_detail["Weight"].isna().sum())

    fighter_detail["Weight"] = fighter_detail.apply(lambda row: int(row["Weight"].split()[0]) if type(row["Weight"]) == str else get_weight(row["fighter_name"]), axis=1)

    print(fighter_detail["Weight"].value_counts())
    print(fighter_detail["Weight"].isna().sum())

if __name__ == '__main__':
    main()
