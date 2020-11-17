import os
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


PATH = os.getcwd()

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

print(list(fight_data))

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

#Within the height coloumn there are two float types
fight_data["RED_Height"] = fight_data["RED_Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)
fight_data["BLUE_Height"] = fight_data["BLUE_Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)
print(fight_data.iloc[0])