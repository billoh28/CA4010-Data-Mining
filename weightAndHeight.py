import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from degree_1 import sanitation_degree_1

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

fig, (ax1, ax2) = plt.subplots(2,1)

fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))


fighter_detail.dropna(axis=0, how='any', inplace=True)

# Prior
fighter_detail["Height"] = fighter_detail["Height"].apply(lambda x: (int(x.split()[0].split("'")[0])*12 + int(x.split()[1].split('"')[0])) if type(x) == str else 0)
fighter_detail["Weight"] = fighter_detail["Weight"].apply(lambda x: int(x.split()[0]) if type(x) == str else x)

# Post
new_fighter_detail = sanitation_degree_1()

# Remove 800 pound man


fighter_detail.plot.scatter(x='Height', y='Weight', c='b', ax=ax1, label="Before")
new_fighter_detail.plot.scatter(x='Height', y='Weight', c='r', ax=ax2, label="After")

#fighter_detail = sanitation_degree_1()
#print(fighter_detail["Height"].mean())
#print(fighter_detail["Height"].mode())
#print(fighter_detail["Height"].median())
#fighter_detail.plot.scatter(x='Height', y='Reach',c='DarkBlue',ax=ax2)

ax1.set_yticks([50, 100, 150, 200, 250, 300, 350, 400, 450])
ax2.set_yticks([50, 100, 150, 200, 250, 300, 350, 400, 450])
plt.show()
