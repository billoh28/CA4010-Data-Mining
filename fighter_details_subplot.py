import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ufc_model import sanitation

fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))

fight_data = sanitation(2) # for age

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

sns.set()
sns.set(style="darkgrid")

age = pd.concat([fight_data['RED_Age'], fight_data['BLUE_Age']], ignore_index=True)

#stance = pd.concat([fighter_detail['Stance']], ignore_index=True)
#stance = stance.dropna(axis=0, how='any')

reach = fighter_detail["Reach"].apply(lambda x: int(x.split('"')[0]) if type(x) == str else x)
reach = reach.dropna(axis=0, how='any')

height = fighter_detail["Height"].apply(lambda x: (int(x.strip('"').split("' ")[0]) * 12) + int(x.strip('"').split("' ")[1]) if type(x) == str else x)
height = height.dropna(axis=0, how='any')

weight = fighter_detail["Weight"].apply(lambda x: int(x.split()[0]) if type(x) == str else x)
weight = weight.dropna(axis=0, how='any')

#print(age.mean())
#print(age.mode())
#print(age.median())

# Plot Age
ax1.hist(age)
ax1.set_xlabel("Index")
ax1.set_ylabel("Age")
ax1.set_xticks(range(18, 50, 2)) 

# Plot Reach
ax2.hist(reach)
ax2.set_xlabel("Index")
ax2.set_ylabel("Reach (Inches)")
ax2.set_xticks(range(50, 85, 2)) 

# Plot Height
ax3.hist(height)
ax3.set_xlabel("Index")
ax3.set_ylabel("Height (Inches)")
ax3.set_xticks(range(50, 85, 2)) 

# Plot Weight
ax4.hist(weight.sort_values(ascending=True))
ax4.set_xlabel("Index")
ax4.set_ylabel("Weight (lbs)")
#ax4.set_xticks(range(100, 400, 10)) 

plt.show()
