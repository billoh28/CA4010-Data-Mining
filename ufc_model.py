import os
import numpy as np
import pandas as pd

fighter_details = pd.read_csv("UFCDataset/raw_fighter_details.csv")
#for some reason one of the files is separated by a semicolon
fight_data = pd.read_csv("UFCDataset/raw_total_fight_data.csv", sep=';')
print(fight_data.info())
