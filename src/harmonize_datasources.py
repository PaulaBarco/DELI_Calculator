""" Harmonizing the datasources to obtain the food item resolution needed

Author: Paula Barco

Date: 2024-02-06

"""

#%%
import pandas as pd
import os
from pathlib import Path
import project_functions as pfuncs
from constants import data_path


save_path = (
    data_path
    / "interim"
)


#Reading the Clean Poore & Nemecek database
poore_nemecek = pfuncs.dataset_reader('clean_poore_and_nemecek.xls', 'interim', 
                             False)


#Reading the food item detail for each food group defined in Poore & Nemecek
fooditem_foodgroup = pfuncs.dataset_reader('ingredient_foogroup.xlsx', 'interim', False)

#Merging the two previous databases to obtain the impacts per food item
fooditem_poore_and_nemecek = pd.merge(poore_nemecek, fooditem_foodgroup, on=['Food group'])

print(fooditem_poore_and_nemecek)

#Moving the Ingredient column to the beginning of the database
col_ingredients = fooditem_poore_and_nemecek.pop('Ingredient')
fooditem_poore_and_nemecek.insert(0, 'Ingredient', col_ingredients)

print(fooditem_poore_and_nemecek)

# Saving the database created in the interim folder
fooditem_poore_and_nemecek.to_excel(save_path / 'food_item_poore_and_nemecek.xlsx', index=False)

# %%
