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
        # Read the Recipe_Template and save the new file with the impacts
        file_path = os.path.join(recipe_directory, file_name)
        save_path = (data_path
        / "impacts"
        )
        recipe_data = pd.read_excel(file_path)
        
        #From the Recipe_template, we abstracted the rows with values 
        abstracted_Lomo_saltado = recipe_data[recipe_data['Amount'].notna()]

        print(abstracted_Lomo_saltado)


        #! Convert_all_to_grams

        # Selected the rows that has different values than grams, so the conversion can be performed
        non_grams = abstracted_Lomo_saltado[abstracted_Lomo_saltado['Unit'] != 'grams']

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
        ingredients_lomo_saltado = pd.merge(non_grams, Conversion_factors, on=['Ingredient', 'Unit'], how='left')

        #Some adjustments so we can have the correct amount in the dataframe (example: 
        #2 tbsp of Olive oil multiplied by the conversion factor)
        ingredients_lomo_saltado['Grams_x'] = ingredients_lomo_saltado['Amount_x']*ingredients_lomo_saltado['Grams']

        #Cleaning process by removing columns not needed anymore
        ingredients_lomo_saltado = ingredients_lomo_saltado.drop(columns = ['Amount_x', 'Unit', 'Amount_y', 'Grams', 'Source'])

        #we now merge the correct amounts for the ingredients with units different than grams and the 
        # ingredients with grams
        recipe_lomo_saltado_wnan = pd.merge(ingredients_lomo_saltado, abstracted_Lomo_saltado, on=['Ingredient'], how='right')

        # More cleaning, first, identify rows where 'Unit' is 'grams' and 'Grams' is NaN, and then
        # replace the NaN values in the 'Grams' column with the corresponding 'Amount_x' values
        m = (recipe_lomo_saltado_wnan['Unit'] == 'grams') & (recipe_lomo_saltado_wnan['Grams_x'].isna())
        recipe_lomo_saltado_wnan.loc[m, 'Grams_x'] = recipe_lomo_saltado_wnan.loc[m, 'Amount']

        #Cleaning dropping specific columns and rows with NaN
        recipe_lomo_saltado = recipe_lomo_saltado_wnan.drop(columns = ['Ingredient', 'Amount', 'Unit'])
        recipe_lomo_saltado = recipe_lomo_saltado.dropna()

        #Cleaning, rename the column 'Grams'
        recipe_lomo_saltado = (
            recipe_lomo_saltado.rename(columns={'Grams_x':'Grams'}))


        #! Impacts_calculation


        #Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(['Olive oil','Onions', 'Tomatoes','Potatoes', 'Rice','Beef'])]
        Recipe_impacts_df = fooditem_PooreNemecek.loc[fooditem_PooreNemecek['Ingredient'].isin(recipe_lomo_saltado_wnan['Ingredient'])]


        #Substract only the columns related to impacts
        Recipe_impacts_df2 = Recipe_impacts_df.loc[:,'Land Use (m2) Arable':'Str-Wt WU (L eq)'].reset_index(drop=True)

        #We create an array with the values from the recipe so we can multiply every row
        #from the impacts dataframe with the corresponding value from the recipe

        Scalar = recipe_lomo_saltado.values
        Scalar_size = Scalar.size

        print(Scalar)

        #Multiplication
        lomo_saltado_impacts = Recipe_impacts_df2.mul(Scalar, axis= 0)

        ### If 1000 gr has X impact, then new amount multiplied by the impact and 
        ## divided by 1000 gr
        lomo_saltado_impacts = lomo_saltado_impacts / 1000

        #We sum the columns to get a total value for each impact
        lomo_saltado_impacts_total = lomo_saltado_impacts.sum()


        # Transpose the row of labels to a column
        #labels_column = Recipe_impacts_df2.iloc[0].to_frame().transpose()

        # Assign the transposed row as a new column in the original DataFrame
        #lomo_saltado_impacts_total['Impacts'] = labels_column.iloc[0]

        # Construct the file path for the output Excel file with a unique numerical suffix
        output_file_path = os.path.splitext(save_path)[0] + f'_impacts_{file_suffix}.xlsx'
        
        # Save the results to an Excel file
        lomo_saltado_impacts_total.to_excel(output_file_path, index=False)
        
        print(f"Environmental impacts saved to {output_file_path}")
        
        # Increment the file suffix for the next iteration
        file_suffix += 1
        




# %%
print(lomo_saltado_impacts_total)
# %%
