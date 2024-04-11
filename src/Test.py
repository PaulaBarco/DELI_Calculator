""" Code to calculate the impact of the different recipes

Author: Paula Barco

Date: 2024-02-06

"""



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

#%%
# Counter to keep track of the file suffix
file_suffix = 1

#%%
# Loop through each Excel file in the folder Recipes
for file_name in os.listdir(recipe_directory):
    if file_name.endswith('.xlsx'):
        # Read the Recipe_Template 
        file_path = os.path.join(recipe_directory, file_name)
        
        recipe_data = pd.read_excel(file_path)
        
        #From the Recipe_template, we abstracted the rows with values 
        abstracted_recipe = recipe_data.dropna()

        print(abstracted_recipe)


        #! Convert_all_to_grams

        # Selected the rows that has different values than grams, so the conversion can be performed
        non_grams = abstracted_recipe[abstracted_recipe['Unit'] != 'grams']

        print(non_grams)

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


        #Then we merge the two dataframes so we can later multiply the amount needed by the 
        # conversion factor
        ingredients_abstracted_recipe = pd.merge(non_grams, Conversion_factors, on=['Ingredient', 'Unit'], how='left')

        #Some adjustments so we can have the correct amount in the dataframe (example: 
        #2 tbsp of Olive oil multiplied by the conversion factor)
        ingredients_abstracted_recipe['Grams_x'] = ingredients_abstracted_recipe['Amount_x']*ingredients_abstracted_recipe['Grams']

        #Cleaning process by removing columns not needed anymore
        ingredients_abstracted_recipe = ingredients_abstracted_recipe.drop(columns = ['Amount_x', 'Unit', 'Amount_y', 'Grams', 'Source'])

        #we now merge the correct amounts for the ingredients with units different than grams and the 
        # ingredients with grams
        recipe_wnan = pd.merge(ingredients_abstracted_recipe, abstracted_recipe, on=['Ingredient'], how='right')

        # More cleaning, first, identify rows where 'Unit' is 'grams' and 'Grams' is NaN, and then
        # replace the NaN values in the 'Grams' column with the corresponding 'Amount_x' values
        m = (recipe_wnan['Unit'] == 'grams') & (recipe_wnan['Grams_x'].isna())
        recipe_wnan.loc[m, 'Grams_x'] = recipe_wnan.loc[m, 'Amount']

        #Cleaning dropping specific columns and rows with NaN
        recipe_final = recipe_wnan.drop(columns = ['Ingredient', 'Amount', 'Unit'])
        recipe_final = recipe_final.dropna()

        #Cleaning, rename the column 'Grams'
        recipe_final = (
            recipe_final.rename(columns={'Grams_x':'Grams'}))


        #! Impacts_calculation


        #Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(['Olive oil','Onions', 'Tomatoes','Potatoes', 'Rice','Beef'])]
        ingredients = abstracted_recipe['Ingredient'].tolist()

        print(ingredients)

        ingredients_impacts = fooditem_PooreNemecek[fooditem_PooreNemecek['Ingredient'].isin(ingredients)]
        
       #Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(recipe_wnan['Ingredient'])]


        #Substract only the columns related to impacts
        Recipe_impacts_df2 = ingredients_impacts.loc[:,'Land Use (m2) Arable':'Str-Wt WU (L eq)'].reset_index(drop=True)

        #We create an array with the values from the recipe so we can multiply every row
        #from the impacts dataframe with the corresponding value from the recipe

        Scalar = recipe_final.values
        Scalar_size = Scalar.size

        print(Scalar)

        #Multiplication
        recipe_impacts_mult = Recipe_impacts_df2.mul(Scalar, axis= 0)

        ### If 1000 gr has X impact, then new amount multiplied by the impact and 
        ## divided by 1000 gr
        recipe_impacts_final = recipe_impacts_mult / 1000

        #We sum the columns to get a total value for each impact
        recipe_impacts_final_total = recipe_impacts_final.sum()

        # Transpose the row of labels to a column
        #labels_column = Recipe_impacts_df2.iloc[0].to_frame().transpose()
        

        # Assign the transposed row as a new column in the original DataFrame
        #lomo_saltado_impacts_total['Impacts'] = labels_column.iloc[0]
        
        # Save the results to an Excel file
        recipe_impacts_final_total.to_excel(save_path_impacts / f'impacts_recipe_{file_suffix}.xlsx', index=False)
        
        print(f"Environmental impacts saved to {save_path_impacts}")

        # Increment the file suffix for the next iteration
        file_suffix += 1
        


   
#%%

# Create a file with the labels to the rows (impacts categories labels)
row_labels = [
    'Land Use (m2) Arable',
    'Land Use (m2) Fallow',
    'Land Use (m2) Perm Past',
    'GHG (kg CO2eq, IPCC 2013) LUC',
    'GHG (kg CO2eq, IPCC 2013) Feed',
    'GHG (kg CO2eq, IPCC 2013) Farm',
    'GHG (kg CO2eq, IPCC 2013) Processing',
    'GHG (kg CO2eq, IPCC 2013) Transport',
    'GHG (kg CO2eq, IPCC 2013) Packging',
    'GHG (kg CO2eq, IPCC 2013) Retail',
    'Acid.(kg SO2eq)',
    'Eutr. (kg PO43-eq)',
    'Freshwater (L)',
    'Str-Wt WU (L eq)'
]

labels_df = pd.DataFrame(row_labels)

print(labels_df)

#%%

labels_df.to_excel(save_path_impacts / 'Impacts_labels.xlsx', index=False)


#%%

excel_files = [file for file in os.listdir(save_path_impacts) if file.endswith('.xlsx')]

print(excel_files)

#%%
# Create an empty DataFrame
df_empty = pd.DataFrame()

print(df_empty)

#%%
# Iterate over each Excel file
for file in excel_files:
    # Read the first column of the Excel file
    df_column = pd.read_excel(os.path.join(save_path_impacts, file), usecols=[0])
    
    # Add the column to the empty DataFrame
    df_empty[file] = df_column.iloc[:, 0]  # Use iloc to ensure it's a Series, not DataFrame
    



print(df_empty)


#%%

df_empty.columns = df_empty.columns.str.replace('.xlsx', '')


#%%
save_path_test = (
    data_path
    / "interim"
)
# Save the results to an Excel file
df_empty.to_excel(save_path_test / 'Impacts_recipes.xlsx', index=False)
        





# %%

#! Calculations per recipe per ingredient


