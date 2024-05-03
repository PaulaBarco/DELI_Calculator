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


#Read the Clean Poore & Nemecek database
fooditem_PooreNemecek = pfuncs.dataset_reader('Fooditem_PooreNemecek.xlsx', 'interim', 
                             False)

#Read the conversion factors for cups, tbsp, tsp, etc.
Conversion_factors = pfuncs.dataset_reader('Conversion_factors.xlsx', 'interim', 
                             False)

# Counter to keep track of the file suffix
file_suffix_recipe = 1

file_suffix_ingredient = 1

# Loop through each Excel file in the folder Recipes
for file_name in os.listdir(recipe_directory):
    if file_name.endswith('.xlsx'):
        # Read all the Recipe_Template 
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

        print(ingredients_abstracted_recipe)

                #Some adjustments so we can have the correct amount in the dataframe (example: 
                #2 tbsp of Olive oil multiplied by the conversion factor)
        ingredients_abstracted_recipe['Grams_x'] = ingredients_abstracted_recipe['Amount_x']*ingredients_abstracted_recipe['Grams']

        print(ingredients_abstracted_recipe)

                #Cleaning process by removing columns not needed anymore
        ingredients_abstracted_recipe = ingredients_abstracted_recipe.drop(columns = ['Amount_x', 'Unit', 'Amount_y', 'Grams', 'Source'])

        print(ingredients_abstracted_recipe)
                #we now merge the correct amounts for the ingredients with units different than grams and the 
                # ingredients with grams

        recipe_wnan = pd.merge(ingredients_abstracted_recipe, abstracted_recipe, on=['Ingredient'], how='right')

                # More cleaning, first, identify rows where 'Unit' is 'grams' and 'Grams' is NaN, and then
                # replace the NaN values in the 'Grams' column with the corresponding 'Amount_x' values

        print(recipe_wnan)

        m = (recipe_wnan['Unit'] == 'grams') & (recipe_wnan['Grams_x'].isna())
        recipe_wnan.loc[m, 'Grams_x'] = recipe_wnan.loc[m, 'Amount']


                #Cleaning dropping specific columns and rows with NaN
        recipe_final = recipe_wnan.drop(columns = ['Amount', 'Unit'])
        recipe_final = recipe_final.dropna()

        print(recipe_final)

        #Cleaning, rename the column 'Grams'
        recipe_final = (
            recipe_final.rename(columns={'Grams_x':'Grams'}))

        print(recipe_final)


                #! Impacts_calculation

        #Merging the ingredients amounts with their corresponding impacts
        ingredients_impacts = pd.merge(recipe_final, fooditem_PooreNemecek, on= 'Ingredient', how= 'left')

        print(ingredients_impacts)


        #Substract only the columns related to impacts
        Recipe_impacts = ingredients_impacts.loc[:,'Ingredient':'Str-Wt WU (L eq)'].reset_index(drop=True)

        print(Recipe_impacts)
        
        #Multiplication of the amounts and the impacts

        Recipe_impacts['Land Use (m2) Arable_x'] = Recipe_impacts['Land Use (m2) Arable']*Recipe_impacts['Grams']
        Recipe_impacts['Land Use (m2) Fallow_x'] = Recipe_impacts['Land Use (m2) Fallow']*Recipe_impacts['Grams']
        Recipe_impacts['Land Use (m2) Perm Past_x'] = Recipe_impacts['Land Use (m2) Perm Past']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) LUC_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) LUC']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Feed_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Feed']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Farm_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Farm']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Processing_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Processing']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Transport_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Transport']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Packging_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Packging']*Recipe_impacts['Grams']
        Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Retail_x'] = Recipe_impacts['GHG (kg CO2eq, IPCC 2013) Retail']*Recipe_impacts['Grams']
        Recipe_impacts['Acid.(kg SO2eq)_x'] = Recipe_impacts['Acid.(kg SO2eq)']*Recipe_impacts['Grams']
        Recipe_impacts['Eutr. (kg PO43-eq)_x'] = Recipe_impacts['Eutr. (kg PO43-eq)']*Recipe_impacts['Grams']
        Recipe_impacts['Freshwater (L)_x'] = Recipe_impacts['Freshwater (L)']*Recipe_impacts['Grams']
        Recipe_impacts['Str-Wt WU (L eq)_x'] = Recipe_impacts['Str-Wt WU (L eq)']*Recipe_impacts['Grams']

        print(Recipe_impacts)

        #Turning the matrix into a DataFrame
        Recipe_impacts = pd.DataFrame(Recipe_impacts)


        #Selecting only the columns that has numeric values
        numeric_columns = Recipe_impacts.select_dtypes(include=[pd.np.number]).columns

        print(numeric_columns)

        #Divide the columns by 1000
        Recipe_impacts[numeric_columns] = Recipe_impacts[numeric_columns].div(1000)

        print(Recipe_impacts)

        #Dropping the original columns - whatever has _ing in the name is because is done for the 
        # ingredient_impacts files

        Recipe_impacts_ing = Recipe_impacts

        Recipe_impacts_ing = Recipe_impacts.drop(columns = ['Grams', 'Food and Waste', 'Food group',
                                                        'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail',
                                                        'Acid.(kg SO2eq)',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Freshwater (L)',
                                                        'Str-Wt WU (L eq)'])


        Recipe_impacts = Recipe_impacts.drop(columns = ['Grams', 'Food and Waste', 'Ingredient', 'Food group',
                                                        'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail',
                                                        'Acid.(kg SO2eq)',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Freshwater (L)',
                                                        'Str-Wt WU (L eq)'])

        #Change of names of the new columns
        Recipe_impacts_ing = (
            Recipe_impacts_ing.rename(columns={'Land Use (m2) Arable_x':'Land Use Arable',
                                        'Land Use (m2) Fallow_x':'Land Use Fallow',
                                        'Land Use (m2) Perm Past_x':'Land Use Perm Past',
                                        'GHG (kg CO2eq, IPCC 2013) LUC_x':'GHG LUC',
                                        'GHG (kg CO2eq, IPCC 2013) Feed_x':'GHG Feed',
                                        'GHG (kg CO2eq, IPCC 2013) Farm_x':'GHG Farm',
                                        'GHG (kg CO2eq, IPCC 2013) Processing_x':'GHG Processing',
                                        'GHG (kg CO2eq, IPCC 2013) Transport_x':'GHG Transport',
                                        'GHG (kg CO2eq, IPCC 2013) Packging_x':'GHG Packging',
                                        'GHG (kg CO2eq, IPCC 2013) Retail_x':'GHG Retail',
                                        'Acid.(kg SO2eq)_x':'Acidification',
                                        'Eutr. (kg PO43-eq)_x':'Eutrophication',
                                        'Freshwater (L)_x':'Freshwater Withdrawals (FW)',
                                        'Str-Wt WU (L eq)_x':'Scarcity-Weighted FW'}))
        
        
        Recipe_impacts = (
            Recipe_impacts.rename(columns={'Land Use (m2) Arable_x':'Land Use Arable',
                                        'Land Use (m2) Fallow_x':'Land Use Fallow',
                                        'Land Use (m2) Perm Past_x':'Land Use Perm Past',
                                        'GHG (kg CO2eq, IPCC 2013) LUC_x':'GHG LUC',
                                        'GHG (kg CO2eq, IPCC 2013) Feed_x':'GHG Feed',
                                        'GHG (kg CO2eq, IPCC 2013) Farm_x':'GHG Farm',
                                        'GHG (kg CO2eq, IPCC 2013) Processing_x':'GHG Processing',
                                        'GHG (kg CO2eq, IPCC 2013) Transport_x':'GHG Transport',
                                        'GHG (kg CO2eq, IPCC 2013) Packging_x':'GHG Packging',
                                        'GHG (kg CO2eq, IPCC 2013) Retail_x':'GHG Retail',
                                        'Acid.(kg SO2eq)_x':'Acidification',
                                        'Eutr. (kg PO43-eq)_x':'Eutrophication',
                                        'Freshwater (L)_x':'Freshwater Withdrawals (FW)',
                                        'Str-Wt WU (L eq)_x':'Scarcity-Weighted FW'}))

        print(Recipe_impacts)

        # Add a Recipe column with the Recipe identifier
        Recipe_impacts_ing['Recipe'] = f'{file_name[:-5]}'
        
        # Save the results per ingredient to an Excel file
        Recipe_impacts_ing.to_excel(save_path_impacts / f'{file_name[:-5]}_impacts_per_ingredient.xlsx', index=False)
        
        # Increment the file suffix for the next iteration
        file_suffix_ingredient += 1

        #Summing up the impacts per category
        recipe_impacts_total = Recipe_impacts.sum()

        print(recipe_impacts_total)
        
        # Save the results to an Excel file
        recipe_impacts_total.to_excel(save_path_impacts / f'Recipe {file_name[:-5]}.xlsx', index=False)
        
        print(f"Environmental impacts saved to {save_path_impacts}")

        # Increment the file suffix for the next iteration
        file_suffix_recipe += 1
        




# Create a file with the labels to the rows (impacts categories labels)
row_labels = [
    'Land Use Arable',
    'Land Use Fallow',
    'Land Use Perm Past',
    'GHG LUC',
    'GHG Feed',
    'GHG Farm',
    'GHG Processing',
    'GHG Transport',
    'GHG Packging',
    'GHG Retail',
    'Acidification',
    'Eutrophication',
    'Freshwater Withdrawals (FW)',
    'Scarcity-Weighted FW'
]

labels_df = pd.DataFrame(row_labels)

print(labels_df)

#Save a file with the impact labels

labels_df.to_excel(save_path_impacts / 'Impacts_labels.xlsx', index=False)


# List all the files that are in the Impact folder
excel_files = [file for file in os.listdir(save_path_impacts) if file.startswith('Recipe') and file.endswith('.xlsx')]

print(excel_files)
# Add the "labels.xlsx" file if it exists
if 'Impacts_labels.xlsx' in os.listdir(save_path_impacts):
    excel_files.append('Impacts_labels.xlsx')

# Create an empty DataFrame
df_empty = pd.DataFrame()

print(df_empty)

# Iterate over each Excel file
for file in excel_files:
    # Read the first column of the Excel file
    df_column = pd.read_excel(os.path.join(save_path_impacts, file), usecols=[0])
    
    # Add the column to the empty DataFrame
    df_empty[file] = df_column.iloc[:, 0]  # Use iloc to ensure it's a Series, not DataFrame
    
print(df_empty)

#Remove the .xlsx from the recipe label in the columns

df_empty.columns = df_empty.columns.str.replace('.xlsx', '')

#Move the Impacts_labels column to the beginning of the database
col_ingredients = df_empty.pop('Impacts_labels')
df_empty.insert(0, 'Impacts_labels', col_ingredients)


save_path_test = (
    data_path
    / "interim"
)
# Save the results to an Excel file
df_empty.to_excel(save_path_test / 'Impacts_recipes.xlsx', index=False)
        
# List all Excel files in the directory that start with 'impact_ingredients'
excel_files_ing = [file for file in os.listdir(save_path_impacts) if file.endswith('impacts_per_ingredient.xlsx')]

print(excel_files_ing)


# Create an empty DataFrame to store the concatenated DataFrames
concatenated_impacts_ing = pd.DataFrame()

# Iterate over the Excel files
for file in excel_files_ing:
    # Load the Excel file into a DataFrame
    df_ing = pd.read_excel(os.path.join(save_path_impacts, file))
    
    # Concatenate the DataFrame with the existing concatenated DataFrame
    concatenated_impacts_ing = pd.concat([concatenated_impacts_ing, df_ing], ignore_index=True)

print(concatenated_impacts_ing)

concatenated_impacts_ing.to_excel(save_path_test / 'Impacts_per_ingredients.xlsx', index=False)

#%%

#! IMPACT CATEGORIES TOTALS

#Read the Clean Poore & Nemecek database
recipe_impacts_test = pfuncs.dataset_reader('Impacts_recipes.xlsx', 'interim', 
                             False)

# Find rows containing GHG emissions
ghg_rows = recipe_impacts_test['Impacts_labels'].str.contains('GHG')

print(ghg_rows)
# Sum rows with GHG emissions into one row
recipe_impacts_test.loc['Total GHG Emissions'] = recipe_impacts_test.loc[ghg_rows].sum()

print(recipe_impacts_test)

recipe_impacts_test.set_index('Impacts_labels', inplace=True)

# Rows to remove (based on their labels/index values)
rows_to_remove = ['GHG LUC', 
                  'GHG Feed',
                  'GHG Farm',
                  'GHG Processing',
                  'GHG Transport',
                  'GHG Packging',
                  'GHG Retail']

recipe_impacts_test = recipe_impacts_test.drop(index=rows_to_remove)

print(recipe_impacts_test)

# Reset index before summing Land Use rows
recipe_impacts_test.reset_index(inplace=True)

LU_rows = recipe_impacts_test['Impacts_labels'].str.contains('Land Use')


# Sum rows with GHG emissions into one row
recipe_impacts_test.loc['Total Land Use'] = recipe_impacts_test.loc[LU_rows].sum()


recipe_impacts_test.set_index('Impacts_labels', inplace=True)

# Rows to remove (based on their labels/index values)
rows_to_remove2 = ['Land Use Arable', 
                 'Land Use Fallow',
                'Land Use Perm Past']

recipe_impacts_test = recipe_impacts_test.drop(index=rows_to_remove2)

print(recipe_impacts_test)


impacts_labels = [
    'Acidification',
    'Eutrophication',
    'Freshwater Withdrawals (FW)',
    'Scarcity-Weighted FW',
    'GHG emissions',
    'Land use']

recipe_impacts_test.insert(0, 'Impacts_labels', impacts_labels)


recipe_impacts_test.to_excel(save_path_test / 'Impacts_total.xlsx', index=False)
# %%
