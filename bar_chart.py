import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load in fight data
fight_data = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_total_fight_data.csv"), sep=';')

# Remove nans
fight_data = fight_data.dropna(axis=0, how='any')

print(fight_data["win_by"].value_counts())

# Make a bar chart of all the different decisions and their counts
# fight_data["win_by"]

data = fight_data["win_by"].value_counts()
data = data.apply(lambda x: int(x))

sns.barplot(x=data, y=data.index, palette='rocket_r')

plt.title('Barchart Showing Disparity Fight Results')
plt.xlabel("No. of Occurances")
plt.tight_layout()

plt.show()
