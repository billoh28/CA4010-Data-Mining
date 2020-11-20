import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from degree_1 import sanitation_degree_1
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

fig, (ax1, ax2) = plt.subplots(1,2)

fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))
fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_total_fight_data.csv"), sep=';')


fighter_detail.dropna(axis=0, how='any', inplace=True)

fighter_detail["Height"] = fighter_detail["Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)
fighter_detail["Reach"] = fighter_detail["Reach"].apply(lambda x: int(x.split('"')[0]) if type(x) == str else 0)



fighter_detail.plot.scatter(x='Height',
                      y='Reach',
                      c='DarkBlue',
                      ax=ax1)

fighter_detail = sanitation_degree_1()
print(fighter_detail["Height"].mean())
print(fighter_detail["Height"].mode())
print(fighter_detail["Height"].median())
fighter_detail.plot.scatter(x='Height',
                      y='Reach',
                      c='DarkBlue',
                      ax=ax2)



plt.show()
