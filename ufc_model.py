import os
import numpy as np
import pandas as pd

PATH = os.getcwd()

fighter_details = pd.read_csv(os.path.join("UFCDataset", "raw_fighter_details.csv"))
#for some reason this file is separated by a semicolon
fight_data = pd.read_csv(os.path.join("UFCDataset", "raw_total_fight_data.csv"), sep=';')

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

print(fight_data.head())