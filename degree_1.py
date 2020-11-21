import os, math
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def multiple_of_five_conv(x):
    weight = int(x.split()[0])
    suffix = x.split()[1:]

    # Convert to multiple of five
    rm = weight % 5

    if rm > 2:
        # Round down
        return " ".join([str(weight - rm)] + suffix)

    elif rm == 0:
        return x

    else:
        # Round up
        return " ".join([str(weight + (10 - rm))] + suffix)

def get_new_weight(row, average_w2h_dict):
    try:
        return str(average_w2h_dict[row["Weight"]])
    except:
        return row["Height"]

def sanitation_degree_1():
    # degree 0 : No sanitation
    # degree 1 : Slight sanitation
    # degree 2 : Complete sanitation

    PATH = os.getcwd()

    fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))
    #for some reason this file is separated by a semicolon

    # Middle severity sanitation
    # Average all the data we can
    # Such as stance, height and reach
    # fighter_detail.dropna(axis=0, how='any', inplace=True)
    # Do this before the merge --> not taking out fighters, just udating their values

    # Stance - Find the mode of all stances in raw_fighter_details.csv
    # print(fighter_detail["Stance"].value_counts(dropna=False)) # --> Orthodox is the most common
    
    stance_mode = fighter_detail["Stance"].mode()
    
    # Now must set every NaN to the mode
    fighter_detail["Stance"] = fighter_detail["Stance"].apply(lambda x: x if type(x) == str else stance_mode[0])
    fighter_detail["Weight"] = fighter_detail["Weight"].apply(lambda x: int(x.split()[0]) if type(x) == str else x)
    fighter_detail["Reach"] = fighter_detail["Reach"].apply(lambda x: int(x.split('"')[0]) if type(x) == str else x)

    # print(fighter_detail["Stance"].value_counts(dropna=False))

    # Now move on to height
    # Must deal with weight first --> 75 NaN weights
    # Can deal with ones which have weight or height, but not neither
    # Need to get the average height for every five pounds of weight, and get average weight for every height
    #print(fighter_detail["Weight"].value_counts(sort=True, dropna=False))
    #print(fighter_detail["Height"].value_counts(sort=True, dropna=False))

    # Must convert heights to inches
    fighter_detail["Height"] = fighter_detail["Height"].apply(lambda x: (int(x.strip('"').split("' ")[0]) * 12) + int(x.strip('"').split("' ")[1]) if type(x) == str else x)

    temp = fighter_detail.iloc[:,1:3] # Copy weight and height colums

    # Make every weight a multiple of five
    temp["Weight"] = temp["Weight"].apply(lambda x: multiple_of_five_conv(x) if type(x) == str else x)

    # Now add in missing weights and heights
    # If a weight is missing, find the coresponding height and vice versa
    #temp = temp.apply(lambda row: weight_from_height(row, temp) if type(row["Weight"]) == float else x)

    # Gonna build a weight to height dictionary
    weight_to_height = {}

    for index, row in temp.iterrows():
        #print(row["Weight"], row["Height"])
        # Need to check if either are NaNs

        if pd.isna(row["Height"]) or pd.isna(row["Weight"]):
            continue
        
        else:
            weight = int(row["Weight"])
            height = int(row["Height"])

            if weight < 265:
                if weight not in weight_to_height:
                    weight_to_height[weight] = [height]
                else:
                    (weight_to_height[weight]).append(height)

    # Now must go through each item in the dictionary and get the average height
    # Make a new dictionary as this one might be useful
    average_w2h_dict = {}
    for key, value_lst in weight_to_height.items():
        # Get average of value_lst
        avg = sum(value_lst)//len(value_lst)

        # Add to dict
        average_w2h_dict[key] = avg

    average_w2h_dict[130] = 66 # 125 --> 65, 135 --> 67

    # print(sorted(average_w2h_dict.keys()))
    # fighter_detail["Height"] = fighter_detail.apply(lambda row: row["Height"] if type(row["Height"]) == str else get_new_weight(row, average_w2h_dict))

    #print(fighter_detail["Height"].value_counts(sort=True, dropna=False))

    # Have all possible heights. Now must fill in missing weights
    # Can use weight_to_height dict to do this
    average_h2w_dict = {}
    for key, value in average_w2h_dict.items():
        average_h2w_dict[value] = key

    #print(average_h2w_dict.keys())

    for index, row in fighter_detail.iterrows():
        if pd.isna(row["Height"]) and pd.isna(row["Weight"]):
            continue

        elif pd.isna(row["Height"]):
            try:
                # Change weight to int and make it a multiple of five
                weight = int(row["Weight"])

                # Change height from nan to an average
                fighter_detail.at[index, "Height"] = int(average_w2h_dict[weight])
            except KeyError: # Over 265 lbs
                fighter_detail.at[index, "Height"] = 80

        elif pd.isna(row["Weight"]):
            try:
                # Change height to inches (from "5' 4""")
                height = int(row["Height"])

                # Change height from nan to an average
                fighter_detail.at[index, "Weight"] = int(average_h2w_dict[height])
            
            except KeyError: # Over or equal 265 lbs
                fighter_detail.at[index, "Weight"] = 265

    #print(fighter_detail["Height"].value_counts(sort=True, dropna=False))
    #print(fighter_detail["Weight"].value_counts(sort=True, dropna=False))

    # Finally --> Reach
    # Reach - "71"""
    height_to_reach = {}

    for index, row in fighter_detail.iterrows():
        #print(row["Weight"], row["Height"])
        # Need to check if either are NaNs

        if pd.isna(row["Height"]) or pd.isna(row["Weight"]):
            continue
        
        elif not pd.isna(row["Reach"]):
            height = int(row["Height"])
            reach = int(row["Reach"])

            if height not in height_to_reach:
                height_to_reach[height] = [reach]

            else:
                height_to_reach[height].append(reach)

    for key, item in height_to_reach.items():
        height_to_reach[key] = sum(item)//len(item)

    # From this we seen that on average reach = height + 1, in inches

    for index, row in fighter_detail.iterrows():
        if pd.isna(row["Height"]) and pd.isna(row["Weight"]):
            continue

        elif pd.isna(row["Reach"]):
            if int(row["Height"]) in height_to_reach:
                fighter_detail.at[index, "Reach"] = height_to_reach[int(row["Height"])]

            else:
                fighter_detail.at[index, "Reach"] = int(row["Height"]) + 1

    #print(fighter_detail.iloc[209:213,])

    return fighter_detail


sanitation_degree_1()