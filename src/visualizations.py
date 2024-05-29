#%%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import project_functions as pfuncs
from constants import data_path
from constants import save_path_impacts

data_recipe = pfuncs.dataset_reader('impacts_recipes.xlsx', 'interim', 
                             False)

#%%
#!SPIDER WEB CHART - Relative environmental performance of recipes

plt.style.use('ggplot')

# Sample data (replace with your own data)
data_test = pfuncs.dataset_reader('impacts_total.xlsx', 'interim', False)
data_test = pd.DataFrame(data_test)

# Extract category column
categories = data_test['impacts_labels']

# Extract recipe columns dynamically
recipe_columns = data_test.columns[1:]  # Exclude the 'Impacts_labels' column

# Identify the recipe with the highest value for each category
highest_values = data_test[recipe_columns].max(axis=1)

# Divide all values by the value of the highest recipe and optionally multiply by 100
scaled_values = data_test[recipe_columns].div(highest_values, axis=0) * 100

# Concatenate the 'Impacts_labels' column with the scaled values DataFrame
scaled_data_with_labels = pd.concat([categories, scaled_values], axis=1)

# Extract columns for the radar chart
impacts = scaled_data_with_labels['impacts_labels'].tolist()
recipes_data = scaled_data_with_labels.drop(columns='impacts_labels')

print(scaled_data_with_labels)

# Number of recipes
num_recipes = scaled_values.shape[1]

# Compute angles
angles = np.linspace(0, 2*np.pi, len(impacts), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

# Drop the first impact label after concatenating it with the last one
impacts.append(impacts[0])

# Ensure the lengths of impacts and angles match
if len(impacts) != len(angles):
    raise ValueError("The number of impacts labels does not match the number of angles.")

# Plot the radar chart
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(polar=True, facecolor='#f0f0f0')

for i, recipe_name in enumerate(recipe_columns):
    values = scaled_data_with_labels.iloc[:, i+1].tolist()
    values.append(values[0])  # Close the loop
    ax.plot(angles, values, '--', label=recipe_name)  # Use recipe name as label
    ax.fill(angles, values, alpha=0.1)

ax.set_thetagrids(angles*180/np.pi, impacts)

# Set the color and transparency of the grid lines
ax.xaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.8, color='darkgrey')  # Adjust color to dark grey

# Adjust the z-order for the grid lines to be higher than the z-order of the subplot
ax.xaxis.grid(zorder=2)  # Set zorder to 2

plt.title(f'Relative environmental performance of recipes', y=1.05, fontweight='bold')

# Set the z-order for the axis labels to be higher than the z-order of the grid lines
ax.set_thetagrids(angles*180/np.pi, impacts, zorder=3)  # Set zorder to 3

plt.grid(True)
plt.tight_layout()
plt.legend(loc='lower right', bbox_to_anchor=(0.05, 0.05), fontsize='small')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'spider_web_chart.png'), bbox_inches='tight')

plt.show()

# %%
#?? 100% STACKED BAR CHART WITH THE DIFFERENT IMPACT CATEGORIES, BUT 
#?? PER RECIPE AND INGREDIENT
#The purpose of the chart is to show the impacts per ingredient per recipe for 
#each impact category

# Reading the data broken down into ingredients
data_stacked_ing = pfuncs.dataset_reader('impacts_per_ingredients.xlsx', 'interim', 
                             False)

df_stacked_ing = pd.DataFrame(data_stacked_ing)

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

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

    print(df_percent_ing)
    
    # Plotting the stacked bar chart
    ax = df_percent_ing.plot(kind='bar', stacked=True, figsize=(12, 8), linewidth=1, color=custom_colors[:len(df_percent_ing.columns)])
    
    # Set background color to white
    ax.set_facecolor('white')

    # Adding labels and title
    plt.title(f'Environmental Impacts Distribution by ingredient - {recipe}', y=1.05, fontweight='bold')
    plt.xlabel('Impact Category')
    plt.ylabel('Percentage')

    # Set axis lines to black
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    
    # Rotate x-axis labels by 45 degrees
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)

    # Displaying the legend
    legend = plt.legend(title='Ingredients', loc='upper left', bbox_to_anchor=(1, 1), frameon=True, edgecolor='black', )
    legend.get_frame().set_facecolor('none')  # Remove filling color

    # Saving the plot
    plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_100_recipes_ing_{recipe}.png'), bbox_inches='tight')
    
    # Showing the plot
    plt.show()



#%%
#?? STACKED BAR CHART PER INGREDIENT FOR THE SAME IMPACT CATEGORY
#The purpose of this chart is to compare the recipes considering all the different ingredients per categories

#For each category, a break down into the ingredients of the recipe with
# the highest impact is shown

#! GHG

# Reading the data
df_stacked_GHG = data_recipe

#Filtering to show only GHG emissions subcategories
df_stacked_GHG = df_stacked_GHG[df_stacked_GHG['impacts_labels'].str.contains('GHG')]

df_stacked_GHG = pd.DataFrame(df_stacked_GHG)

print(df_stacked_GHG)

# Setting 'Impacts_labels' column as index
df_stacked_GHG.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_GHG.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Adding labels and title
plt.title('GHG Emissions by Lifecycle Stage and Recipe', y=1.05, fontweight='bold')
plt.xlabel('Lifecycle Stage')
plt.ylabel('GHG Emissions (Kg CO2 eq)')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)  # Rotate labels and align them to the right

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1),  frameon=True, edgecolor='black',)
legend.get_frame().set_facecolor('none')  # Remove filling color

# Adjust the layout to make space for the title
plt.tight_layout()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_GHG.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%
#* Impact for the recipe with the highest impact per ingredient
#Now, the user can zoom in into the details (ingredients) for the recipe with the highest impact

# Finding the recipe with the highest impact
highest_impact_recipe_GHG = df_stacked_GHG.max().idxmax()

print(highest_impact_recipe_GHG)

#Reading the data
df_stacked_ing_GHG = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_GHG = df_stacked_ing_GHG[df_stacked_ing_GHG['Recipe'].str.startswith(highest_impact_recipe_GHG[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_GHG = filtered_df_stacked_ing_GHG.drop(columns = ['Recipe',
                                                        'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past', 
                                                        'Acidification',
                                                        'Eutrophication',
                                                        'Freshwater Withdrawals (FW)',
                                                        'Scarcity-Weighted FW'])

#Setting the column Ingredient as index
filtered_df_stacked_ing_GHG.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_GHG = filtered_df_stacked_ing_GHG.T

print(df_stacked_transposed_GHG)

# Plotting the stacked bar chart
ax = df_stacked_transposed_GHG.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)  # Rotate labels and align them to the right

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'GHG emissions by ingredient - {highest_impact_recipe_GHG}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('Kg CO2 eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Adjust the layout to make space for the title
plt.tight_layout()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_GHG_{highest_impact_recipe_GHG}.png', bbox_inches='tight'))

# Showing the plot
plt.show()

#%%
#! Land Use

#Reading the data
df_stacked_LU = data_recipe

#Filtering to show only Land Use subcategories
df_stacked_LU = df_stacked_LU[df_stacked_LU['impacts_labels'].str.contains('Land Use')]

df_stacked_LU = pd.DataFrame(df_stacked_LU)

print(df_stacked_LU)

# Setting 'Impacts labels' column as index
df_stacked_LU.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_LU.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Land Use by Land type and Recipe', y=1.05, fontweight='bold')
plt.xlabel('Land types')
plt.ylabel('m2')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1),  frameon=True, edgecolor='black',)
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_LU.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_LU = df_stacked_LU.max().idxmax()

print(highest_impact_recipe_LU)

#Reading the data
df_stacked_ing_LU = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_LU = df_stacked_ing_LU[df_stacked_ing_LU['Recipe'].str.startswith(highest_impact_recipe_LU[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_LU = filtered_df_stacked_ing_LU.drop(columns = ['Recipe', 'GHG LUC', 
                                                        'GHG Feed',
                                                        'GHG Farm',
                                                        'GHG Processing',
                                                        'GHG Transport',
                                                        'GHG Packging',
                                                        'GHG Retail', 
                                                        'Acidification',
                                                        'Eutrophication',
                                                        'Freshwater Withdrawals (FW)',
                                                        'Scarcity-Weighted FW'])

filtered_df_stacked_ing_LU.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_LU = filtered_df_stacked_ing_LU.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_LU.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Land use by ingredient - {highest_impact_recipe_LU}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('m2')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_LU_{highest_impact_recipe_LU}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%
#! Acidification

#Reading the data
df_stacked_Acd = data_recipe

#Filtering to show only Acidification
df_stacked_Acd = df_stacked_Acd[df_stacked_Acd['impacts_labels'].str.contains('Acid')]

df_stacked_Acd = pd.DataFrame(df_stacked_Acd)

print(df_stacked_Acd)

# Setting 'Impacts_labels' column as index
df_stacked_Acd.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_Acd.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Acidification by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('kg SO2eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Acd.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Acd = df_stacked_Acd.max().idxmax()

print(highest_impact_recipe_Acd)

#Reading the data
df_stacked_ing_Acd = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Acd = df_stacked_ing_Acd[df_stacked_ing_Acd['Recipe'].str.startswith(highest_impact_recipe_Acd[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Acd = filtered_df_stacked_ing_Acd.drop(columns = ['Recipe', 'GHG LUC', 
                                                        'GHG Feed',
                                                        'GHG Farm',
                                                        'GHG Processing',
                                                        'GHG Transport',
                                                        'GHG Packging',
                                                        'GHG Retail', 'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past',
                                                        'Eutrophication',
                                                        'Freshwater Withdrawals (FW)',
                                                        'Scarcity-Weighted FW'])

filtered_df_stacked_ing_Acd.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Acd = filtered_df_stacked_ing_Acd.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_Acd.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Acidification by ingredient - {highest_impact_recipe_Acd}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('kg SO2eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Acd_{highest_impact_recipe_Acd}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#! Eutrophication

#Reading the data
df_stacked_Eut = data_recipe

#Filtering to show only Eutrophication
df_stacked_Eut = df_stacked_Eut[df_stacked_Eut['impacts_labels'].str.contains('Eutr')]

df_stacked_Eut = pd.DataFrame(df_stacked_Eut)

print(df_stacked_Eut)

# Setting 'Impact labels' column as index
df_stacked_Eut.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_Eut.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Eutrophication by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('kg PO43-eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Eut.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Eut = df_stacked_Eut.max().idxmax()

print(highest_impact_recipe_Eut)

#Reading the data
df_stacked_ing_Eut = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Eut = df_stacked_ing_Eut[df_stacked_ing_Eut['Recipe'].str.startswith(highest_impact_recipe_Eut[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Eut = filtered_df_stacked_ing_Eut.drop(columns = ['Recipe', 'GHG LUC', 
                                                        'GHG Feed',
                                                        'GHG Farm',
                                                        'GHG Processing',
                                                        'GHG Transport',
                                                        'GHG Packging',
                                                        'GHG Retail', 'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past',
                                                        'Acidification',
                                                        'Freshwater Withdrawals (FW)',
                                                        'Scarcity-Weighted FW'])

filtered_df_stacked_ing_Eut.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Eut = filtered_df_stacked_ing_Eut.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_Eut.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Eutrophication by ingredient - {highest_impact_recipe_Eut}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('kg PO43-eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color
    
# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Eut_{highest_impact_recipe_Eut}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#! Freshwater

#Reading the data
df_stacked_FW = data_recipe

#Filtering to show only Freshwater
df_stacked_FW = df_stacked_FW[df_stacked_FW['impacts_labels'].str.contains('Freshwater')]

df_stacked_FW = pd.DataFrame(df_stacked_FW)

print(df_stacked_FW)

# Setting 'Impacts_labels' column as index
df_stacked_FW.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_FW.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12) 

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Freshwater by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('Liters')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_FW.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_FW = df_stacked_FW.max().idxmax()

print(highest_impact_recipe_FW)

#Reading the data
df_stacked_ing_FW = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_FW = df_stacked_ing_FW[df_stacked_ing_FW['Recipe'].str.startswith(highest_impact_recipe_FW[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_FW = filtered_df_stacked_ing_FW.drop(columns = ['Recipe', 'GHG LUC', 
                                                        'GHG Feed',
                                                        'GHG Farm',
                                                        'GHG Processing',
                                                        'GHG Transport',
                                                        'GHG Packging',
                                                        'GHG Retail', 'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past',
                                                        'Acidification',
                                                        'Eutrophication',
                                                        'Scarcity-Weighted FW'])

filtered_df_stacked_ing_FW.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_FW = filtered_df_stacked_ing_FW.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_FW.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)
 
# Adding labels and title
plt.title(f'Freshwater by ingredient - {highest_impact_recipe_FW}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('Liters')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_FW_{highest_impact_recipe_FW}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%


#! Str-Wt WU

#Reading the data
df_stacked_Str = data_recipe

#Filtering to show only Str-Wt WU
df_stacked_Str = df_stacked_Str[df_stacked_Str['impacts_labels'].str.contains('Scarcity-Weighted')]

df_stacked_Str = pd.DataFrame(df_stacked_Str)

print(df_stacked_Str)

# Setting 'Impact_labels' column as index
df_stacked_Str.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_Str.plot(kind='bar', figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12) 

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Scarcity-Weighted FW by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('Liters eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Str.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%
#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_Str = df_stacked_Str.max().idxmax()

print(highest_impact_recipe_Str)

#Reading the data
df_stacked_ing_Str = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_Str = df_stacked_ing_Str[df_stacked_ing_Str['Recipe'].str.startswith(highest_impact_recipe_Str[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_Str = filtered_df_stacked_ing_Str.drop(columns = ['Recipe', 'GHG LUC', 
                                                        'GHG Feed',
                                                        'GHG Farm',
                                                        'GHG Processing',
                                                        'GHG Transport',
                                                        'GHG Packging',
                                                        'GHG Retail', 'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past',
                                                        'Acidification',
                                                        'Eutrophication',
                                                        'Freshwater Withdrawals (FW)'])

filtered_df_stacked_ing_Str.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_Str = filtered_df_stacked_ing_Str.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_Str.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set background color to white
ax.set_facecolor('white')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Set y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Scarcity-Weighted FW by ingredient - {highest_impact_recipe_Str}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('Liters eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')  # Remove filling color

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Str_{highest_impact_recipe_Str}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%
#! RESULTS FROM THE SURVEY

from matplotlib.ticker import MaxNLocator

data_survey = pfuncs.dataset_reader('results_survey.xlsx', 'interim', 
                             False)


df_survey = pd.DataFrame(data_survey)

#Removing the impact categories not needed for this chart
filtered_df_survey= df_survey.drop(columns = ['Marca temporal', 'Is there anything that you want to highlight from this prototype?', 
                                                        'Are there any comments or suggestions that can help us improve the user experience and prototype?'])

# Define the full range of Likert scale options
likert_scale = [1, 2, 3, 4, 5]

# Calculate the frequency of each response for each question
response_counts = filtered_df_survey.apply(pd.Series.value_counts).reindex(likert_scale, fill_value=0)

# Define colors to match the provided chart (adjust as needed based on the actual colors in the provided chart)
colors = {
    1: "#1f77b4",  # Blue
    2: "#ff7f0e",  # Orange
    3: "#2ca02c",  # Green
    4: "#d62728",  # Red
    5: "#9467bd"   # Purple
}

# Plot a bar chart for each question
for question in filtered_df_survey.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plotting the bar chart with matching colors
    bars = ax.bar(response_counts.index, response_counts[question], color=[colors[i] for i in response_counts.index], edgecolor='black')
    
    # Set background color to white
    ax.set_facecolor('white')

    # Set axis lines to black
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')

    # Rotate x-axis labels by 0 degrees
    ax.set_xticks(likert_scale)
    ax.set_xticklabels(likert_scale, rotation=0, ha='center', fontsize=12)

    # Set y-axis labels with increased font size
    ax.set_yticklabels(ax.get_yticks(), fontsize=12)

    # Set y-axis to show only full numbers
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Adding labels and title
    plt.title(f'{question}', y=1.05, fontweight='bold')
    plt.xlabel('Likert Scale')
    plt.ylabel('Frequency')

    # Showing the plot
    plt.show()



# %%
import pkg_resources

# List of libraries to check
libraries = [
    'pandas',
    'pathlib',
    'os',
    'numpy',
    'matplotlib'
]

# Function to check library versions
def check_versions(libraries):
    for lib in libraries:
        try:
            version = pkg_resources.get_distribution(lib).version
            print(f"{lib}: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"{lib} is not installed")

check_versions(libraries)
# %%
