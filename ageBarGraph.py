import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ufc_model import sanitation

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

fighter_detail = pd.read_csv(os.path.join("UFCDataset", "Original", "raw_fighter_details.csv"))

fight_data = sanitation(2)
sns.set()
sns.set(style="darkgrid")

age = pd.concat([fight_data['RED_Age'], fight_data['BLUE_Age']], ignore_index=True)
print(age.mean())
print(age.mode())
print(age.median())

age_values = age.value_counts()
age_labels = age_values.index

sns.barplot(x=age_labels,y=age_values)
plt.title('Histogram Showing Dispersion of Age')
plt.ylabel('Number of Fighters')
plt.xlabel('Age')
plt.show()