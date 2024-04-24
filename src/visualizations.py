#%%
import pandas as pd
import os
import matplotlib.pyplot as plt
import ProjectFunctions as pfuncs
from constants import data_path
from constants import save_path_impacts

#%%

#?? 100% STACKED BAR CHART
#The purpose of this chart is to compare the recipes considering all the different impact categories

# Reading the data
data_recipe = pfuncs.dataset_reader('Impacts_recipes.xlsx', 'interim', 
                             False)

df_100stacked = pd.DataFrame(data_recipe)

#Setting the impacts as index to calculate the relative weights for each value per impact category
df_100stacked.set_index('Impacts_labels', inplace=True)

df_percent = df_100stacked.div(df_100stacked.sum(axis=1), axis=0) * 100


# Plotting the stacked bar chart
df_percent.plot(kind='bar', stacked=True, figsize=(12, 8))

# Adding labels and title
plt.title('Environmental Impacts Distribution by Recipe')
plt.xlabel('Impact Category')
plt.ylabel('Percentage')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_100_recipes.png'))

# %%


#?? 100% STACKED BAR CHART WITH THE DIFFERENT IMPACT CATEGORIES, BUT 
#?? PER RECIPE AND INGREDIENT
#The purpose of the chart is to show the impacts per ingredient per recipe for 
#each impact category

# Reading the data broken down into ingredients
data_stacked_ing = pfuncs.dataset_reader('Impacts_per_ingredients.xlsx', 'interim', 
                             False)

df_stacked_ing = pd.DataFrame(data_stacked_ing)

#Removing the rows with the subtotals
df_stacked_ing = df_stacked_ing[df_stacked_ing['Ingredient'] != 'Total']


# Loop for iterating over each recipe in order to get visualizations with the ingredients breakdown
for recipe in df_stacked_ing['Recipe'].unique():
    # Filtering DataFrame for the current recipe
    filtered_df = df_stacked_ing[df_stacked_ing['Recipe'] == recipe]
    
    # Removing the 'Recipe' column
    filtered_df = filtered_df.drop(columns=['Recipe'])
    
    # Setting 'Ingredient' column as index
    filtered_df.set_index('Ingredient', inplace=True)
    
    # Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
    df_transposed = filtered_df.T
    
    # Calculating percentages
    df_percent_ing = df_transposed.div(df_transposed.sum(axis=1), axis=0) * 100
    
    # Plotting the stacked bar chart
    df_percent_ing.plot(kind='bar', stacked=True, figsize=(12, 8))
    
    # Adding labels and title
    plt.title(f'Environmental Impacts Distribution by ingredient - {recipe}')
    plt.xlabel('Impact Category')
    plt.ylabel('Percentage')
    
    # Displaying the legend
    plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
    # Showing the plot
    plt.show()

    # Saving the plot
    plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_100_recipes_ing_{recipe}.png'))



#%%
#?? STACKED BAR CHART PER INGREDIENT FOR THE SAME IMPACT CATEGORY
#The purpose of this chart is to compare the recipes considering all the different ingredients per categories

#For each category, a break down into the ingredients of the recipe with
# the highest impact is shown

#! GHG

# Reading the data
df_stacked_GHG = data_recipe

#Filtering to show only GHG emissions subcategories
df_stacked_GHG = df_stacked_GHG[df_stacked_GHG['Impacts_labels'].str.contains('GHG')]

df_stacked_GHG = pd.DataFrame(df_stacked_GHG)

# Setting 'Impacts_labels' column as index
df_stacked_GHG.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_GHG.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('GHG Emissions by Lifecycle Stage and Recipe')
plt.xlabel('Lifecycle Stage')
plt.ylabel('GHG Emissions (Kg CO2 eq)')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_GHG.png'))

#%%
#* Impact for the recipe with the highest impact per ingredient
#Now, the user can zoom in into the details (ingredients) for the recipe with the highest impact

# Finding the recipe with the highest impact
highest_impact_recipe_GHG = df_stacked_GHG.max().idxmax()

print(highest_impact_recipe_GHG)

#Reading the data
df_stacked_ing_GHG = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_GHG = df_stacked_ing_GHG[df_stacked_ing_GHG['Recipe'] == highest_impact_recipe_GHG]

#Removing the subtotal columns
filtered_df_stacked_ing_GHG = filtered_df_stacked_ing_GHG[filtered_df_stacked_ing_GHG['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_GHG = filtered_df_stacked_ing_GHG.drop(columns = ['Recipe',
                                                        'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past', 
                                                        'Acid.(kg SO2eq)',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Freshwater (L)',
                                                        'Str-Wt WU (L eq)'])

#Setting the column Ingredient as index
filtered_df_stacked_ing_GHG.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_GHG = filtered_df_stacked_ing_GHG.T

# Plotting the stacked bar chart
df_stacked_transposed_GHG.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'GHG emissions by ingredient - {highest_impact_recipe_GHG}')
plt.xlabel('Impact Category')
plt.ylabel('Kg CO2 eq')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_GHG_{highest_impact_recipe_GHG}.png'))



#%%
#! Land Use

#Reading the data
df_stacked_LU = data_recipe

#Filtering to show only Land Use subcategories
df_stacked_LU = df_stacked_LU[df_stacked_LU['Impacts_labels'].str.contains('Land Use')]

df_stacked_LU = pd.DataFrame(df_stacked_LU)

# Setting 'Impacts labels' column as index
df_stacked_LU.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_LU.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('Land Use by Land type and Recipe')
plt.xlabel('Land types')
plt.ylabel('m2')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_LU.png'))

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_LU = df_stacked_LU.max().idxmax()

print(highest_impact_recipe_LU)

#Reading the data
df_stacked_ing_LU = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_LU = df_stacked_ing_LU[df_stacked_ing_LU['Recipe'] == highest_impact_recipe_LU]

#Removing the subtotal columns
filtered_df_stacked_ing_LU = filtered_df_stacked_ing_LU[filtered_df_stacked_ing_LU['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_LU = filtered_df_stacked_ing_LU.drop(columns = ['Recipe', 'GHG (kg CO2eq, IPCC 2013) LUC', 
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

filtered_df_stacked_ing_LU.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_LU = filtered_df_stacked_ing_LU.T

# Plotting the stacked bar chart
df_stacked_transposed_LU.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'Land use by ingredient - {highest_impact_recipe_LU}')
plt.xlabel('Impact Category')
plt.ylabel('m2')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_LU_{highest_impact_recipe_LU}.png'))




#%%
#! Acidification

#Reading the data
df_stacked_Acd = data_recipe

#Filtering to show only Acidification
df_stacked_Acd = df_stacked_Acd[df_stacked_Acd['Impacts_labels'].str.contains('Acid')]

df_stacked_Acd = pd.DataFrame(df_stacked_Acd)

# Setting 'Impacts_labels' column as index
df_stacked_Acd.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_Acd.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('Acidification by Recipe')
plt.xlabel('Acidification')
plt.ylabel('kg SO2eq')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_Acd.png'))

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Acd = df_stacked_Acd.max().idxmax()

print(highest_impact_recipe_Acd)

#Reading the data
df_stacked_ing_Acd = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Acd = df_stacked_ing_Acd[df_stacked_ing_Acd['Recipe'] == highest_impact_recipe_Acd]

#Removing the subtotal columns
filtered_df_stacked_ing_Acd = filtered_df_stacked_ing_Acd[filtered_df_stacked_ing_Acd['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Acd = filtered_df_stacked_ing_Acd.drop(columns = ['Recipe', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail', 'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Freshwater (L)',
                                                        'Str-Wt WU (L eq)'])

filtered_df_stacked_ing_Acd.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Acd = filtered_df_stacked_ing_Acd.T

# Plotting the stacked bar chart
df_stacked_transposed_Acd.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'Acidification by ingredient - {highest_impact_recipe_LU}')
plt.xlabel('Impact Category')
plt.ylabel('kg SO2eq')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_Acd_{highest_impact_recipe_Acd}.png'))


#%%

#! Eutrophication

#Reading the data
df_stacked_Eut = data_recipe

#Filtering to show only Eutrophication
df_stacked_Eut = df_stacked_Eut[df_stacked_Eut['Impacts_labels'].str.contains('Eutr')]

df_stacked_Eut = pd.DataFrame(df_stacked_Eut)

# Setting 'Impact labels' column as index
df_stacked_Eut.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_Eut.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('Eutrophication by Recipe')
plt.xlabel('Eutrophication')
plt.ylabel('kg PO43-eq')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_Eut.png'))

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Eut = df_stacked_Eut.max().idxmax()

print(highest_impact_recipe_Eut)

#Reading the data
df_stacked_ing_Eut = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Eut = df_stacked_ing_Eut[df_stacked_ing_Eut['Recipe'] == highest_impact_recipe_Eut]

#Removing the subtotal columns
filtered_df_stacked_ing_Eut = filtered_df_stacked_ing_Eut[filtered_df_stacked_ing_Eut['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Eut = filtered_df_stacked_ing_Eut.drop(columns = ['Recipe', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail', 'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past',
                                                        'Acid.(kg SO2eq)',
                                                        'Freshwater (L)',
                                                        'Str-Wt WU (L eq)'])

filtered_df_stacked_ing_Eut.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Eut = filtered_df_stacked_ing_Eut.T

# Plotting the stacked bar chart
df_stacked_transposed_Eut.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'Eutrophication by ingredient - {highest_impact_recipe_Eut}')
plt.xlabel('Impact Category')
plt.ylabel('kg PO43-eq')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_Eut_{highest_impact_recipe_Eut}.png'))



#%%

#! Freshwater

#Reading the data
df_stacked_FW = data_recipe

#Filtering to show only Freshwater
df_stacked_FW = df_stacked_FW[df_stacked_FW['Impacts_labels'].str.contains('Freshwater')]

df_stacked_FW = pd.DataFrame(df_stacked_FW)

# Setting 'Impacts_labels' column as index
df_stacked_FW.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_FW.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('Freshwater by Recipe')
plt.xlabel('Freshwater')
plt.ylabel('Liters')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_FW.png'))

#%%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_FW = df_stacked_FW.max().idxmax()

print(highest_impact_recipe_FW)

#Reading the data
df_stacked_ing_FW = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_FW = df_stacked_ing_FW[df_stacked_ing_FW['Recipe'] == highest_impact_recipe_FW]

#Removing the subtotal columns
filtered_df_stacked_ing_FW = filtered_df_stacked_ing_FW[filtered_df_stacked_ing_FW['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_FW = filtered_df_stacked_ing_FW.drop(columns = ['Recipe', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail', 'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past',
                                                        'Acid.(kg SO2eq)',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Str-Wt WU (L eq)'])

filtered_df_stacked_ing_FW.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_FW = filtered_df_stacked_ing_FW.T

# Plotting the stacked bar chart
df_stacked_transposed_FW.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'Freshwater by ingredient - {highest_impact_recipe_Eut}')
plt.xlabel('Impact Category')
plt.ylabel('Liters')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_FW_{highest_impact_recipe_FW}.png'))


# %%


#! Str-Wt WU

#Reading the data
df_stacked_Str = data_recipe

#Filtering to show only Str-Wt WU
df_stacked_Str = df_stacked_Str[df_stacked_Str['Impacts_labels'].str.contains('Str-Wt WU')]

df_stacked_Str = pd.DataFrame(df_stacked_Str)

# Setting 'Impact_labels' column as index
df_stacked_Str.set_index('Impacts_labels', inplace=True)

# Plotting the multiple bar chart
df_stacked_Str.plot(kind='bar', figsize=(12, 8))

# Adding labels and title
plt.title('Str-Wt WU by Recipe')
plt.xlabel('Str-Wt WU')
plt.ylabel('Liters eq')

# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))

# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'Stacked_bar_recipes_Str.png'))

# %%
#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Str = df_stacked_Str.max().idxmax()

print(highest_impact_recipe_Str)

#Reading the data
df_stacked_ing_Str = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Str = df_stacked_ing_Str[df_stacked_ing_Str['Recipe'] == highest_impact_recipe_Str]

#Removing the subtotal columns
filtered_df_stacked_ing_Str = filtered_df_stacked_ing_Str[filtered_df_stacked_ing_Str['Ingredient'] != 'Total']

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Str = filtered_df_stacked_ing_Str.drop(columns = ['Recipe', 'GHG (kg CO2eq, IPCC 2013) LUC', 
                                                        'GHG (kg CO2eq, IPCC 2013) Feed',
                                                        'GHG (kg CO2eq, IPCC 2013) Farm',
                                                        'GHG (kg CO2eq, IPCC 2013) Processing',
                                                        'GHG (kg CO2eq, IPCC 2013) Transport',
                                                        'GHG (kg CO2eq, IPCC 2013) Packging',
                                                        'GHG (kg CO2eq, IPCC 2013) Retail', 'Land Use (m2) Arable', 'Land Use (m2) Fallow', 
                                                        'Land Use (m2) Perm Past',
                                                        'Acid.(kg SO2eq)',
                                                        'Eutr. (kg PO43-eq)',
                                                        'Freshwater (L)'])

filtered_df_stacked_ing_Str.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Str = filtered_df_stacked_ing_Str.T

# Plotting the stacked bar chart
df_stacked_transposed_Str.plot(kind='bar', stacked=True, figsize=(12, 8))
    
# Adding labels and title
plt.title(f'Str-Wt WU by ingredient - {highest_impact_recipe_Eut}')
plt.xlabel('Impact Category')
plt.ylabel('Liters eq')
    
# Displaying the legend
plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
    
# Showing the plot
plt.show()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'Stacked_bar_Str_{highest_impact_recipe_Str}.png'))

# %%
