import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load in fight data
fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"), sep=',')

# Make a bar chart NaNs occurences

height = fight_data["Height"].isna().sum()
weight = fight_data["Weight"].isna().sum()
reach = fight_data["Reach"].isna().sum()
stance = fight_data["Stance"].isna().sum()
dob = fight_data["DOB"].isna().sum()

data = [reach, stance, dob, height, weight]



sns.barplot(x=["Reach", "Stance", "Date of Birth", "Height", "Weight"], y=data, palette='rocket_r')

plt.title('Barchart Showing No. of NaN Occurences in Fighter Details per Column')
plt.ylabel("No. of Occurances")
plt.tight_layout()

plt.show()
