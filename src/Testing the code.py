

#%%
import pandas as pd
import os
from pathlib import Path
import ProjectFunctions as pfuncs
from constants import data_path
from constants import recipe_directory
from constants import save_path_impacts


#%%
#Substract the section of the Poore&Nemecek database needed for this recipe
#Read the Clean Poore & Nemecek database
fooditem_PooreNemecek = pfuncs.dataset_reader('Fooditem_PooreNemecek.xlsx', 'interim', 
                             False)

#Read the conversion factors for cups, tbsp, tsp, etc.
Conversion_factors = pfuncs.dataset_reader('Conversion_factors.xlsx', 'interim', 
                             False)


recipe_data = pfuncs.dataset_reader('Recipe_template_1.xlsx', 'recipes', 
                             False)
        
        #From the Recipe_template, we abstracted the rows with values 
abstracted_recipe = recipe_data.dropna()

print(abstracted_recipe)

#%%
#! Convert_all_to_grams

        # Selected the rows that has different values than grams, so the conversion can be performed
non_grams = abstracted_recipe[abstracted_recipe['Unit'] != 'grams']

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
ingredients_abstracted_recipe = pd.merge(non_grams, Conversion_factors, on=['Ingredient', 'Unit'], how='left')

print(ingredients_abstracted_recipe)

#%%
        #Some adjustments so we can have the correct amount in the dataframe (example: 
        #2 tbsp of Olive oil multiplied by the conversion factor)
ingredients_abstracted_recipe['Grams_x'] = ingredients_abstracted_recipe['Amount_x']*ingredients_abstracted_recipe['Grams']

print(ingredients_abstracted_recipe)

#%%
        #Cleaning process by removing columns not needed anymore
ingredients_abstracted_recipe = ingredients_abstracted_recipe.drop(columns = ['Amount_x', 'Unit', 'Amount_y', 'Grams', 'Source'])

print(ingredients_abstracted_recipe)
        #we now merge the correct amounts for the ingredients with units different than grams and the 
        # ingredients with grams

#%%
recipe_wnan = pd.merge(ingredients_abstracted_recipe, abstracted_recipe, on=['Ingredient'], how='right')

        # More cleaning, first, identify rows where 'Unit' is 'grams' and 'Grams' is NaN, and then
        # replace the NaN values in the 'Grams' column with the corresponding 'Amount_x' values

print(recipe_wnan)

#%%
m = (recipe_wnan['Unit'] == 'grams') & (recipe_wnan['Grams_x'].isna())
recipe_wnan.loc[m, 'Grams_x'] = recipe_wnan.loc[m, 'Amount']


        #Cleaning dropping specific columns and rows with NaN
recipe_final = recipe_wnan.drop(columns = ['Ingredient', 'Amount', 'Unit'])
recipe_final = recipe_final.dropna()

print(recipe_final)

#%%


        #Cleaning, rename the column 'Grams'
recipe_final = (
    recipe_final.rename(columns={'Grams_x':'Grams'}))

print(recipe_final)

#%%

        #! Impacts_calculation


        #Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(['Olive oil','Onions', 'Tomatoes','Potatoes', 'Rice','Beef'])]
ingredients = abstracted_recipe['Ingredient'].tolist()

print(ingredients)

#%%
ingredients_impacts = fooditem_PooreNemecek[fooditem_PooreNemecek['Ingredient'].isin(ingredients)]


print(ingredients_impacts)

#%%
#Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(recipe_wnan['Ingredient'])]


        #Substract only the columns related to impacts
Recipe_impacts_df2 = ingredients_impacts.loc[:,'Land Use (m2) Arable':'Str-Wt WU (L eq)'].reset_index(drop=True)

print(Recipe_impacts_df2)
        #We create an array with the values from the recipe so we can multiply every row
        #from the impacts dataframe with the corresponding value from the recipe

#%%
Scalar = recipe_final.values
Scalar_size = Scalar.size

print(Scalar)

#%%
        #Multiplication
recipe_impacts_mult = Recipe_impacts_df2.mul(Scalar, axis= 0)


print(recipe_impacts_mult)
#%%

        ### If 1000 gr has X impact, then new amount multiplied by the impact and 
        ## divided by 1000 gr
recipe_impacts_final = recipe_impacts_mult / 1000

print(recipe_impacts_final)

#%%
        #We sum the columns to get a total value for each impact
recipe_impacts_final_total = recipe_impacts_final.sum()

print(recipe_impacts_final_total)
