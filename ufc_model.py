import os
import numpy as np
import pandas as pd
from degree_1 import sanitation_degree_1
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def extract_winner(row):
    # Extract if red or blue won
    red = row["R_fighter"].lower()
    blue = row["B_fighter"].lower()
    winner = row["Winner"].lower()

    # No draws in dataset
    if winner == blue:
        return 1

    return 0


def sanitation(degree=0, is_prior=False):

    PATH = os.getcwd()

    if degree == 1:
        fighter_detail = sanitation_degree_1()

    else:
        fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))
    #for some reason this file is separated by a semicolon
    fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_total_fight_data.csv"), sep=';')



    #Separate the following colunms into two separate coloumns
    #The Original coloumns data looked like:
        #13 of 78
    attemp = '_att'
    landed = '_landed'
    columns = ['R_SIG_STR.', 'B_SIG_STR.', 'R_TOTAL_STR.', 'B_TOTAL_STR.',
           'R_TD', 'B_TD', 'R_HEAD', 'B_HEAD', 'R_BODY','B_BODY', 'R_LEG', 'B_LEG', 
            'R_DISTANCE', 'B_DISTANCE', 'R_CLINCH','B_CLINCH', 'R_GROUND', 'B_GROUND']

    for column in columns:
        fight_data[column+attemp] = fight_data[column].apply(lambda X: int(X.split('of')[1]))
        fight_data[column+landed] = fight_data[column].apply(lambda X: int(X.split('of')[0]))

    #Delete the orginal columns with ofs    
    fight_data.drop(columns, axis=1, inplace=True)

    #Coloumns have percentage, we want fractions
    pct_columns = ['R_SIG_STR_pct','B_SIG_STR_pct', 'R_TD_pct', 'B_TD_pct']

    for column in pct_columns:
        fight_data[column] = fight_data[column].apply(lambda X: float(X.replace('%', ''))/100)


    # Add fighter details to dataset

    fight_data = fight_data.merge(fighter_detail, left_on='R_fighter', right_on='fighter_name', how='left')
    fight_data.drop('fighter_name', axis=1, inplace=True)
    fight_data.rename(columns={'Height':'RED_Height', 'Weight':'RED_Weight', 'Reach':'RED_Reach', 'Stance':'RED_Stance', 'DOB':'RED_DOB'}, inplace=True)


    fight_data = fight_data.merge(fighter_detail, left_on='B_fighter', right_on='fighter_name', how='left')
    fight_data.drop('fighter_name', axis=1, inplace=True)
    fight_data.rename(columns={'Height':'BLUE_Height', 'Weight':'BLUE_Weight', 'Reach':'BLUE_Reach', 'Stance':'BLUE_Stance', 'DOB':'BLUE_DOB'}, inplace=True)

    fight_data.drop("Referee", axis=1, inplace=True) # Drop referee first as it is not needed

    if degree in [1, 2]: fight_data = fight_data.dropna(axis=0, how='any')
    
    #print(list(fight_data["date"]))
    #print(list(fight_data["RED_DOB"])[0].split()[-1])

    def add_age(row, is_blue):
        try:
            if is_blue:
                return int(row["date"].split()[-1]) - int(row["BLUE_DOB"].split()[-1])
            return int(row["date"].split()[-1]) - int(row["RED_DOB"].split()[-1])
        except AttributeError:
            return 0


    # Adding age columns to dataset
    fight_data["RED_Age"] = fight_data.apply(lambda row: add_age(row, False), axis=1)
    fight_data["BLUE_Age"] = fight_data.apply(lambda row: add_age(row, True), axis=1)


    # Dont't need following rows for classification
    fight_data.drop(['date', 'RED_DOB', 'BLUE_DOB', 'location'], axis=1, inplace=True)


    if degree != 1:
        #Within the height coloumn there are two float types
        fight_data["RED_Height"] = fight_data["RED_Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)
        fight_data["BLUE_Height"] = fight_data["BLUE_Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)

        # Remove lbs from weight
        fight_data["RED_Weight"] = fight_data["RED_Weight"].apply(lambda x: int(x.split()[0]) if type(x) == str else 0)
        fight_data["BLUE_Weight"] = fight_data["BLUE_Weight"].apply(lambda x: int(x.split()[0]) if type(x) == str else 0)

        # Remove " from reach
        fight_data["RED_Reach"] = fight_data["RED_Reach"].apply(lambda x: int(x.split('"')[0]) if type(x) == str else 0)
        fight_data["BLUE_Reach"] = fight_data["BLUE_Reach"].apply(lambda x: int(x.split('"')[0]) if type(x) == str else 0)

    # Changing format column to be no. minutes in fight
    #fight_data["Fight_Duration"] = fight_data["Format"].apply(lambda x: int(x.split()[0]) * int(x.split()[-1].split('-')[-1].strip(')').strip('(')) if x.split()[0].isdigit() else 0)
    fight_data["Round_length_mins"] = fight_data["Format"].apply(lambda x: int(x.split()[-1].split('-')[-1].strip(')').strip('(')) if x.split()[0].isdigit() else 0)
    fight_data["Duration"] = fight_data["Format"].apply(lambda x: int(x.split()[0]) * int(x.split()[-1].split('-')[-1].strip(')').strip('(')) if x.split()[0].isdigit() else 0)
    
    fight_data.drop('Format', axis=1, inplace=True)

    # Changing last_round_time format to be in seconds
    fight_data["last_round_time"] = fight_data["last_round_time"].apply(lambda x: (int(x.split(':')[0])*60) + int(x.split(':')[1]) if type(x) == str else 0)

    # Change duration to be last round time + previous rounds
    fight_data["Total_Time"] = fight_data.apply(lambda row: int(row["last_round_time"]) + ((int(row["last_round"])-1) * int(row["Round_length_mins"]) * 60) if type(row["last_round"]) == int else 0, axis=1)

    # Now drop rest
    fight_data.drop('Round_length_mins', axis=1, inplace=True)

    #print(type(fight_data.iloc[0]['R_SIG_STR_pct']))
    #print(fight_data.iloc[999])

    #print(len(fight_data[fight_data['RED_Age'] == 0]))

    #print(fight_data.iloc[0])
    # print(fight_data["BLUE_Age"].value_counts())

    # Change winner to binary value
    

    fight_data["Winner"] = fight_data.apply(lambda row: (extract_winner(row)), axis=1) # extract if winner is red or blue

    # Add winner to end of dataset
    location = fight_data.columns.get_loc("Winner")

    cols = fight_data.columns.tolist()

    cols = cols[:location] + cols[location+1:] + [cols[location]]

    fight_data = fight_data[cols]

    #fight_data.drop("Winner", axis=1, inplace=True)
    
    # After consideration we decided to split the dataset in two
    # We split on whether the model is predicting prior to the fight or after the fight

    if not is_prior:
        # Don't need half the things we have in as we onlt care about what happened in the fight
        # We can also convert the fighters names in red or blue (0, 1)
        
        fight_data.drop("last_round", axis=1, inplace=True)
        fight_data.drop("last_round_time", axis=1, inplace=True)
        fight_data.drop("Fight_type", axis=1, inplace=True)
        fight_data.drop("win_by", axis=1, inplace=True)
        fight_data.drop("R_fighter", axis=1, inplace=True)
        fight_data.drop("B_fighter", axis=1, inplace=True)

        # After removing these columns the accuracy did not change, apart from a percent reduction with win_by for obvious reasons, meaning the models were not using these attributes

        #print(fight_data.iloc[0])

    else:
        # prior prediction
        # Want a dataset with all the fighters stastistics, red and blue, and who won the fight
        # drop all details of the fight and keep evrything which was there before the fight.
        # Still predicting the winner just without the insight of knowing how the fight went.
        # In theory, this will make a model which could predict the outcome of two fighters given their statistics and not the outcome.

        # Convert fighter to red and blue
        #fight_data["R_fighter"] = fight_data["R_fighter"].apply(lambda x: 0)
        #fight_data["B_fighter"] = fight_data["B_fighter"].apply(lambda x: 1)

        fight_data.drop("R_fighter", axis=1, inplace=True)
        fight_data.drop("B_fighter", axis=1, inplace=True)

        # Drop irrelevant columns i.e data from the fight

        # Drop Red & Blue fight data
        fight_data.drop("R_KD", axis=1, inplace=True)
        fight_data.drop("B_KD", axis=1, inplace=True)
        fight_data.drop("R_SIG_STR_pct", axis=1, inplace=True)
        fight_data.drop("B_SIG_STR_pct", axis=1, inplace=True)
        fight_data.drop("R_TD_pct", axis=1, inplace=True)
        fight_data.drop("B_TD_pct", axis=1, inplace=True)
        fight_data.drop("R_SUB_ATT", axis=1, inplace=True)
        fight_data.drop("B_SUB_ATT", axis=1, inplace=True)
        fight_data.drop("R_PASS", axis=1, inplace=True)
        fight_data.drop("B_PASS", axis=1, inplace=True)
        fight_data.drop("R_REV", axis=1, inplace=True)
        fight_data.drop("B_REV", axis=1, inplace=True)
        fight_data.drop("R_SIG_STR._att", axis=1, inplace=True)
        fight_data.drop("B_SIG_STR._att", axis=1, inplace=True)
        fight_data.drop("R_SIG_STR._landed", axis=1, inplace=True)
        fight_data.drop("B_SIG_STR._landed", axis=1, inplace=True)
        fight_data.drop("R_TOTAL_STR._att", axis=1, inplace=True)
        fight_data.drop("B_TOTAL_STR._att", axis=1, inplace=True)
        fight_data.drop("R_TOTAL_STR._landed", axis=1, inplace=True)
        fight_data.drop("B_TOTAL_STR._landed", axis=1, inplace=True)
        fight_data.drop("R_TD_att", axis=1, inplace=True)
        fight_data.drop("B_TD_att", axis=1, inplace=True)
        fight_data.drop("R_TD_landed", axis=1, inplace=True)
        fight_data.drop("B_TD_landed", axis=1, inplace=True)
        
        fight_data.drop("R_HEAD_att", axis=1, inplace=True)
        fight_data.drop("B_HEAD_att", axis=1, inplace=True)
        fight_data.drop("R_HEAD_landed", axis=1, inplace=True)
        fight_data.drop("B_HEAD_landed", axis=1, inplace=True)

        fight_data.drop("R_BODY_att", axis=1, inplace=True)
        fight_data.drop("B_BODY_att", axis=1, inplace=True)
        fight_data.drop("R_BODY_landed", axis=1, inplace=True)
        fight_data.drop("B_BODY_landed", axis=1, inplace=True)

        fight_data.drop("R_DISTANCE_att", axis=1, inplace=True)
        fight_data.drop("B_DISTANCE_att", axis=1, inplace=True)
        fight_data.drop("R_DISTANCE_landed", axis=1, inplace=True)
        fight_data.drop("B_DISTANCE_landed", axis=1, inplace=True)

        fight_data.drop("R_CLINCH_att", axis=1, inplace=True)
        fight_data.drop("B_CLINCH_att", axis=1, inplace=True)
        fight_data.drop("R_CLINCH_landed", axis=1, inplace=True)
        fight_data.drop("B_CLINCH_landed", axis=1, inplace=True)

        fight_data.drop("R_GROUND_att", axis=1, inplace=True)
        fight_data.drop("B_GROUND_att", axis=1, inplace=True)
        fight_data.drop("R_GROUND_landed", axis=1, inplace=True)
        fight_data.drop("B_GROUND_landed", axis=1, inplace=True)

        fight_data.drop("R_LEG_att", axis=1, inplace=True)
        fight_data.drop("B_LEG_att", axis=1, inplace=True)
        fight_data.drop("R_LEG_landed", axis=1, inplace=True)
        fight_data.drop("B_LEG_landed", axis=1, inplace=True)

        # Drop other fight data
        fight_data.drop("last_round", axis=1, inplace=True)
        fight_data.drop("last_round_time", axis=1, inplace=True)
        fight_data.drop("win_by", axis=1, inplace=True)
        fight_data.drop("Referee", axis=1, inplace=True)

    # Remove red fighters so equal number of red and blue winners
    # Go through data and count number of blue winners, add to new dataset. Then add red wineers up until max is reached


    print(fight_data.iloc[0])
    return fight_data


sanitation(degree=1, is_prior=False)