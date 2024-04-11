#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ProjectFunctions as pfuncs
from constants import data_path

#%%
# Sample data
data = pfuncs.dataset_reader('Impacts_recipes.xlsx', 'interim', 
                             False)

#%%

df = pd.DataFrame(data)

# Set 'Recipe' column as index
df.set_index('Impacts_labels', inplace=True)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5)
plt.title('Environmental Impact Heatmap by Recipe')
plt.xlabel('Recipe')
plt.ylabel('Impact')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
