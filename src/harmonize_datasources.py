""" Harmonizing the datasources to obtain the food item resolution needed

Author: Paula Barco

Date: 2024-02-06

"""

#%%
import pandas as pd
import os
from pathlib import Path
import ProjectFunctions as pfuncs
from constants import data_path

#os.getcwd()
#directory_path = Path("..")
save_path = (
    data_path
    / "interim"
)


#Read the Clean Poore & Nemecek database
Poore_nemecek = pfuncs.dataset_reader('Clean_Poore&Nemecek.xls', 'interim', 
                             False)


#Read the food item detail for each food group defined in Poore & Nemecek
fooditem_foodgroup = pfuncs.dataset_reader('ingredient_foogroup.xlsx', 'interim', False)

#Merge the two previous databases to obtain the impacts per food item
fooditem_PooreNemecek = pd.merge(Poore_nemecek, fooditem_foodgroup, on=['Food group'])

print(fooditem_PooreNemecek)

#Move the Ingredient column to the beginning of the database
col_ingredients = fooditem_PooreNemecek.pop('Ingredient')
fooditem_PooreNemecek.insert(0, 'Ingredient', col_ingredients)

print(fooditem_PooreNemecek)

# Save the database created in the interim folder
fooditem_PooreNemecek.to_excel(save_path / 'Fooditem_PooreNemecek.xlsx', index=False)

# %%
