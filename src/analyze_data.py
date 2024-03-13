""" Code to calculate the impact of the different recipes

Author: Paula Barco

Date: 2024-02-06

"""



#%%
import pandas as pd
import os
from pathlib import Path
import ProjectFunctions as pfuncs
import numpy as np

#%%
os.getcwd()
directory_path = Path("..")
save_path = (
    directory_path
    / "data"
    / "interim"
)

#%%
#Read the Clean Poore & Nemecek database
Poore_nemecek = pfuncs.dataset_reader('Clean_Poore&Nemecek.xls', 'interim', 
                             False)

#%%
#Read the food item detail for each food group defined in Poore & Nemecek
fooditem_foodgroup = pfuncs.dataset_reader('ingredient_foogroup.xlsx', 'interim', False)

# %%
#Merge the two previous databases to obtain the impacts per food item
fooditem_PooreNemecek = pd.merge(Poore_nemecek, fooditem_foodgroup, on=['Food group'])

print(fooditem_PooreNemecek)

# %%
#Move the Ingredient column to the beginning of the database
col_ingredients = fooditem_PooreNemecek.pop('Ingredient')
fooditem_PooreNemecek.insert(0, 'Ingredient', col_ingredients)

print(fooditem_PooreNemecek)

#%%
# Save the database created in the interim folder
fooditem_PooreNemecek.to_excel(save_path / 'Fooditem_PooreNemecek.xlsx', index=False)

# %%
##? RECIPE
#Here the calculations for the recipe chosen

#First, we need to read the recipe_template file which has the information about the 
#amounts for the corresponding ingredients (this is something that the user would fill out)

Lomo_saltado = pfuncs.dataset_reader('Recipe_template.xlsx', 'interim', 
                             False)

##* Lomo saltado ingredients
##Vegetable oil - 2 tbsp - for this recipe olive oil was chosen
##Sirloin steak (beef) - 455 grams
##Red onion - 1.5 units
##Tomato - 1 unit
##Garlic - 2 cloves
##Aji amarillo paste - 1 tbsp
##Soy sauce - 2 tbsp
##White vinegar - 1 tbsp
##Cilantro - 1 tbsp
##Potato - 455 grams
##Rice - 1 cup

#%%
#Read the conversion factors for cups, tbsp, tsp, etc.
Conversion_factors = pfuncs.dataset_reader('Conversion_factors.xlsx', 'interim', 
                             False)
#%%
#From the Recipe_template, we abstracted the rows with values 
abstracted_Lomo_saltado = Lomo_saltado[Lomo_saltado['Amount'].notna()]

print(abstracted_Lomo_saltado)


#%%
# Selected the rows that has different values than grams, so the conversion can be performed
non_grams = abstracted_Lomo_saltado[abstracted_Lomo_saltado['Unit'] != 'grams']

print(non_grams)


#%%
#Conversion, for this we iterate over each row in non_grams df and then check the 
#conversion factor from the Conversion_factors df
for index, row in non_grams.iterrows():
    ingredient = row['Ingredient']
    unit = row['Unit']
    
    conversion_factor = Conversion_factors[(Conversion_factors['Ingredient'] == ingredient) & (Conversion_factors['Unit'] == unit)]['Grams'].values
    if len(conversion_factor) > 0:
        print(f"Conversion factor for {ingredient} in {unit}: {conversion_factor[0]} grams")
    else:
        print(f"No conversion factor found for {ingredient} in {unit}")



#%%
#Then we merge the two dataframes so we can later multiply the amount needed by the 
# conversion factor
ingredients_lomo_saltado = pd.merge(non_grams, Conversion_factors, on=['Ingredient', 'Unit'], how='left')

print(ingredients_lomo_saltado)


#%%
#Some adjustments so we can have the correct amount in the dataframe (example: 
#2 tbsp of Olive oil multiplied by the conversion factor)
ingredients_lomo_saltado['Grams_x'] = ingredients_lomo_saltado['Amount_x']*ingredients_lomo_saltado['Grams']

print(ingredients_lomo_saltado)

#%%
#Cleaning process by removing columns not needed anymore
ingredients_lomo_saltado = ingredients_lomo_saltado.drop(columns = ['Amount_x', 'Unit', 'Amount_y', 'Grams', 'Source'])

print(ingredients_lomo_saltado)

#%%
#we now merge the correct amounts for the ingredients with units different than grams and the 
# ingredients with grams
recipe_lomo_saltado = pd.merge(ingredients_lomo_saltado, abstracted_Lomo_saltado, on=['Ingredient'], how='right')

print(recipe_lomo_saltado)


#%%
# More cleaning, first, identify rows where 'Unit' is 'grams' and 'Grams' is NaN, and then
# replace the NaN values in the 'Grams' column with the corresponding 'Amount_x' values
m = (recipe_lomo_saltado['Unit'] == 'grams') & (recipe_lomo_saltado['Grams_x'].isna())
recipe_lomo_saltado.loc[m, 'Grams_x'] = recipe_lomo_saltado.loc[m, 'Amount']

print(recipe_lomo_saltado)

#%%
#Cleaning dropping specific columns and rows with NaN
recipe_lomo_saltado = recipe_lomo_saltado.drop(columns = ['Ingredient', 'Amount', 'Unit'])
recipe_lomo_saltado = recipe_lomo_saltado.dropna()
print(recipe_lomo_saltado)

#%%
#Cleaning, rename the column 'Grams'
recipe_lomo_saltado = (
    recipe_lomo_saltado.rename(columns={'Grams_x':'Grams'}))

print(recipe_lomo_saltado)


#%%
#Substract the section of the Poore&Nemecek database needed for this recipe
Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(['Olive oil','Onions', 'Tomatoes','Potatoes', 'Rice','Beef'])]

print(Recipe_impacts_df)

#%%
#Substract only the columns related to impacts
Recipe_impacts_df2 = Recipe_impacts_df.loc[:,'Land Use (m2) Arable':'Str-Wt WU (L eq)'].reset_index(drop=True)

print(Recipe_impacts_df2)

# %%
#We create an array with the values from the recipe so we can multiply every row
#from the impacts dataframe with the corresponding value from the recipe

Scalar = recipe_lomo_saltado.values

print(Scalar)

#%%
#Multiplication
lomo_saltado_impacts = Recipe_impacts_df2.loc[:5].mul(Scalar, axis= 0)

print(lomo_saltado_impacts)

# %%
### If 1000 gr has X impact, then new amount multiplied by the impact and 
## divided by 1000 gr
lomo_saltado_impacts = lomo_saltado_impacts / 1000

print(lomo_saltado_impacts)
# %%
#We sum the columns to get a total value for each impact
lomo_saltado_impacts_total = lomo_saltado_impacts.sum()

print(lomo_saltado_impacts_total)
# %%
