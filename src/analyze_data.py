#%%
import pandas as pd
import os
from pathlib import Path
import ProjectFunctions as pfuncs

#%%
os.getcwd()
directory_path = Path("..")
save_path = (
    directory_path
    / "data"
    / "interim"
)

#%%


Poore_nemecek = pfuncs.dataset_reader('Clean_Poore&Nemecek.xls', 'interim', 
                             False)

#%%
fooditem_foodgroup = pfuncs.dataset_reader('ingredient_foogroup.xlsx', 'interim', False)

# %%
fooditem_PooreNemecek = pd.merge(Poore_nemecek, fooditem_foodgroup, on=['Food group'])

print(fooditem_PooreNemecek)

# %%
col_ingredients = fooditem_PooreNemecek.pop('Ingredient')
fooditem_PooreNemecek.insert(0, 'Ingredient', col_ingredients)

print(fooditem_PooreNemecek)

#%%
# Save the database created
fooditem_PooreNemecek.to_excel(save_path / 'Fooditem_PooreNemecek.xlsx', index=False)

# %%
