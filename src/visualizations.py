#%%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import project_functions as pfuncs
from constants import data_path
from constants import save_path_impacts

#reading the impacts saved in the previous script
data_recipe = pfuncs.dataset_reader('impacts_recipes.xlsx', 'interim', 
                             False)

#%%
#!SPIDER WEB CHART - Relative environmental performance of recipes
#This chart sets as 100% the recipe with the highest impact per categoty and 
#set the rest of the recipes relative to that impact in percentages.

plt.style.use('ggplot')

# Reading the total impacts, instead of by the breakdown into life cycle
#emissions and land use types
data_test = pfuncs.dataset_reader('impacts_total.xlsx', 'interim', False)
data_test = pd.DataFrame(data_test)

# Extracting category column
categories = data_test['impacts_labels']

# Extracting recipe columns dynamically
recipe_columns = data_test.columns[1:] 

# Identifying the recipe with the highest value for each category
highest_values = data_test[recipe_columns].max(axis=1)

# Dividing all values by the value of the highest recipe and optionally multiply by 100
scaled_values = data_test[recipe_columns].div(highest_values, axis=0) * 100

# Concatenating the 'Impacts_labels' column with the scaled values DataFrame
scaled_data_with_labels = pd.concat([categories, scaled_values], axis=1)

# Extracting columns for the radar chart
impacts = scaled_data_with_labels['impacts_labels'].tolist()
recipes_data = scaled_data_with_labels.drop(columns='impacts_labels')

print(scaled_data_with_labels)

# Number of recipes
num_recipes = scaled_values.shape[1]

# Computating angles
angles = np.linspace(0, 2*np.pi, len(impacts), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

# Drop the first impact label after concatenating it with the last one
impacts.append(impacts[0])

# making sure that the lengths of impacts and angles match
if len(impacts) != len(angles):
    raise ValueError("Do not match")

# Plotting the radar chart
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(polar=True, facecolor='#f0f0f0')

for i, recipe_name in enumerate(recipe_columns):
    values = scaled_data_with_labels.iloc[:, i+1].tolist()
    values.append(values[0]) 
    ax.plot(angles, values, '--', label=recipe_name) 
    ax.fill(angles, values, alpha=0.1)

ax.set_thetagrids(angles*180/np.pi, impacts)

# Set the color and transparency of the grid lines
ax.xaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.8, color='darkgrey')

# Adjusting the order for the grid lines to see the label of the axis
ax.xaxis.grid(zorder=2) 

plt.title(f'Relative environmental performance of recipes', y=1.05, fontweight='bold')

ax.set_thetagrids(angles*180/np.pi, impacts, zorder=3) 

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
    
    # Setting background color to white
    ax.set_facecolor('white')

    # Adding labels and title
    plt.title(f'Environmental Impacts Distribution by ingredient - {recipe}', y=1.05, fontweight='bold')
    plt.xlabel('Impact Category')
    plt.ylabel('Percentage')

    # Set axis lines to black
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    
    # Rotating x-axis labels by 45 degrees
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)

    # Displaying the legend
    legend = plt.legend(title='Ingredients', loc='upper left', bbox_to_anchor=(1, 1), frameon=True, edgecolor='black', )
    legend.get_frame().set_facecolor('none')

    # Saving the plot
    plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_100_recipes_ing_{recipe}.png'), bbox_inches='tight')
    
    # Showing the plot
    plt.show()



#%%
#?? STACKED BAR CHART PER INGREDIENT FOR THE SAME IMPACT CATEGORY
#The purpose of this chart is to compare the recipes considering all the different ingredients per categories

#For each category, a break down into the ingredients of the recipe with
# the highest impact is shown

#! GHG emissions

# Reading the data
df_stacked_ghg = data_recipe

#Filtering to show only GHG emissions subcategories
df_stacked_ghg = df_stacked_ghg[df_stacked_ghg['impacts_labels'].str.contains('GHG')]

df_stacked_ghg = pd.DataFrame(df_stacked_ghg)

print(df_stacked_ghg)

# Setting 'Impacts_labels' column as index
df_stacked_ghg.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_ghg.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Adding labels and title
plt.title('GHG Emissions by Lifecycle Stage and Recipe', y=1.05, fontweight='bold')
plt.xlabel('Lifecycle Stage')
plt.ylabel('GHG Emissions (Kg CO2 eq)')

# Set axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12) 

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1),  frameon=True, edgecolor='black',)
legend.get_frame().set_facecolor('none')  # Remove filling color

# Adjusting the layout to make space for the title
plt.tight_layout()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_GHG.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%
#* Impact for the recipe with the highest impact per ingredient
#Now, the user can zoom in into the details (ingredients) for the recipe with the highest impact

# Finding the recipe with the highest impact
highest_impact_recipe_ghg = df_stacked_ghg.max().idxmax()

print(highest_impact_recipe_ghg)

#Setting up some custom colors since the charts were repeating the same 
#color pallet after the fifth ingredient
custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_ghg = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_ghg = df_stacked_ing_ghg[df_stacked_ing_ghg['Recipe'].str.startswith(highest_impact_recipe_ghg[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_ghg = filtered_df_stacked_ing_ghg.drop(columns = ['Recipe',
                                                        'Land Use Arable', 'Land Use Fallow', 
                                                        'Land Use Perm Past', 
                                                        'Acidification',
                                                        'Eutrophication',
                                                        'Freshwater Withdrawals (FW)',
                                                        'Scarcity-Weighted FW'])

#Setting the column Ingredient as index
filtered_df_stacked_ing_ghg.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_ghg = filtered_df_stacked_ing_ghg.T

print(df_stacked_transposed_ghg)

# Plotting the stacked bar chart
ax = df_stacked_transposed_ghg.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_ghg.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12) 

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'GHG emissions by ingredient - {highest_impact_recipe_ghg}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('kg CO2 eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none') 

# Adjusting the layout to make space for the title
plt.tight_layout()

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_GHG_{highest_impact_recipe_ghg}.png'))

# Showing the plot
plt.show()

#%%
#! Land Use

#Reading the data
df_stacked_lu = data_recipe

#Filtering to show only Land Use subcategories
df_stacked_lu = df_stacked_lu[df_stacked_lu['impacts_labels'].str.contains('Land Use')]

df_stacked_lu = pd.DataFrame(df_stacked_lu)

print(df_stacked_lu)

# Setting 'Impacts labels' column as index
df_stacked_lu.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_lu.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Land Use by Land type and Recipe', y=1.05, fontweight='bold')
plt.xlabel('Land types')
plt.ylabel('m2')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1),  frameon=True, edgecolor='black',)
legend.get_frame().set_facecolor('none') 

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_LU.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_lu = df_stacked_lu.max().idxmax()

print(highest_impact_recipe_lu)

#Setting up some custom colors since the charts were repeating the same 
#color pallet after the fifth ingredient

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_lu = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_lu = df_stacked_ing_lu[df_stacked_ing_lu['Recipe'].str.startswith(highest_impact_recipe_lu[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_lu = filtered_df_stacked_ing_lu.drop(columns = ['Recipe', 'GHG LUC', 
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

filtered_df_stacked_ing_lu.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_lu = filtered_df_stacked_ing_lu.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_lu.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_lu.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Land use by ingredient - {highest_impact_recipe_lu}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('m2')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none') 

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_LU_{highest_impact_recipe_lu}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%
#! Acidification

#Reading the data
df_stacked_acd = data_recipe

#Filtering to show only Acidification
df_stacked_acd = df_stacked_acd[df_stacked_acd['impacts_labels'].str.contains('Acid')]

df_stacked_acd = pd.DataFrame(df_stacked_acd)

print(df_stacked_acd)

# Setting 'Impacts_labels' column as index
df_stacked_acd.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_acd.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Acidification by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('kg SO2eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Acd.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_acd = df_stacked_acd.max().idxmax()

print(highest_impact_recipe_acd)

#Setting up some custom colors since the charts were repeating the same 
#color pallet after the fifth ingredient

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_acd = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_acd = df_stacked_ing_acd[df_stacked_ing_acd['Recipe'].str.startswith(highest_impact_recipe_acd[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_acd = filtered_df_stacked_ing_acd.drop(columns = ['Recipe', 'GHG LUC', 
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

filtered_df_stacked_ing_acd.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_acd = filtered_df_stacked_ing_acd.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_acd.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_acd.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Acidification by ingredient - {highest_impact_recipe_acd}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('kg SO2eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Acd_{highest_impact_recipe_acd}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#! Eutrophication

#Reading the data
df_stacked_eut = data_recipe

#Filtering to show only Eutrophication
df_stacked_eut = df_stacked_eut[df_stacked_eut['impacts_labels'].str.contains('Eutr')]

df_stacked_eut = pd.DataFrame(df_stacked_eut)

print(df_stacked_eut)

# Setting 'Impact labels' column as index
df_stacked_eut.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_eut.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Eutrophication by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('kg PO43-eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Eut.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_eut = df_stacked_eut.max().idxmax()

print(highest_impact_recipe_eut)

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_eut = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_eut = df_stacked_ing_eut[df_stacked_ing_eut['Recipe'].str.startswith(highest_impact_recipe_eut[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_eut = filtered_df_stacked_ing_eut.drop(columns = ['Recipe', 'GHG LUC', 
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

filtered_df_stacked_ing_eut.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_eut = filtered_df_stacked_ing_eut.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_eut.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_eut.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Eutrophication by ingredient - {highest_impact_recipe_eut}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('kg PO43-eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')
    
# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Eut_{highest_impact_recipe_eut}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#! Freshwater

#Reading the data
df_stacked_fw = data_recipe

#Filtering to show only Freshwater
df_stacked_fw = df_stacked_fw[df_stacked_fw['impacts_labels'].str.contains('Freshwater')]

df_stacked_fw = pd.DataFrame(df_stacked_fw)

print(df_stacked_fw)

# Setting 'Impacts_labels' column as index
df_stacked_fw.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_fw.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotate x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12) 

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Freshwater by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('Liters')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none') 

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_FW.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%

#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_fw = df_stacked_fw.max().idxmax()

print(highest_impact_recipe_fw)

#Setting up some custom colors since the charts were repeating the same 
#color pallet after the fifth ingredient

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_fw = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_fw = df_stacked_ing_fw[df_stacked_ing_fw['Recipe'].str.startswith(highest_impact_recipe_fw[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_fw = filtered_df_stacked_ing_fw.drop(columns = ['Recipe', 'GHG LUC', 
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

filtered_df_stacked_ing_fw.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_fw = filtered_df_stacked_ing_fw.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_fw.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_fw.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)
 
# Adding labels and title
plt.title(f'Freshwater by ingredient - {highest_impact_recipe_fw}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('Liters')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_FW_{highest_impact_recipe_fw}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%


#! Scarcity-weighted freshwater withdrawal

#Reading the data
df_stacked_str = data_recipe

#Filtering to show only Str-Wt WU
df_stacked_str = df_stacked_str[df_stacked_str['impacts_labels'].str.contains('Scarcity-Weighted')]

df_stacked_str = pd.DataFrame(df_stacked_str)

print(df_stacked_str)

# Setting 'Impact_labels' column as index
df_stacked_str.set_index('impacts_labels', inplace=True)

# Plotting the multiple bar chart
ax = df_stacked_str.plot(kind='bar', figsize=(12, 8))

# Setting background color to white
ax.set_facecolor('white')

# Setting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12) 

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title('Scarcity-Weighted FW by Recipe', y=1.05, fontweight='bold')
plt.xlabel('Impact category')
plt.ylabel('Liters eq')

# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, 'stacked_bar_recipes_Str.png'), bbox_inches='tight')

# Showing the plot
plt.show()

# %%
#* Impact for the recipe with the highest impact per ingredient

# Finding the recipe with the highest impact
highest_impact_recipe_str = df_stacked_str.max().idxmax()

print(highest_impact_recipe_str)

#Setting up some custom colors since the charts were repeating the same 
#color pallet after the fifth ingredient

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

#Reading the data
df_stacked_ing_str = data_stacked_ing

#Filtering the dataframe by the recipe with the highest impact
filtered_df_stacked_ing_str = df_stacked_ing_str[df_stacked_ing_str['Recipe'].str.startswith(highest_impact_recipe_str[7:])]

#Removing the impact categories not needed for this chart
filtered_df_stacked_ing_str = filtered_df_stacked_ing_str.drop(columns = ['Recipe', 'GHG LUC', 
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

filtered_df_stacked_ing_str.set_index('Ingredient', inplace=True)
  
# Transposing the DataFrame so the data follows the same format as before which is needed for a stacked bar chart
df_stacked_transposed_str = filtered_df_stacked_ing_str.T

# Plotting the stacked bar chart
ax = df_stacked_transposed_str.plot(kind='bar', stacked=True, figsize=(12, 8), color=custom_colors[:len(df_stacked_transposed_str.columns)])

# Setting background color to white
ax.set_facecolor('white')

# Seting axis lines to black
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

# Rotating x-axis labels by 0 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=12)  

# Setting y-axis labels with increased font size
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

# Adding labels and title
plt.title(f'Scarcity-Weighted FW by ingredient - {highest_impact_recipe_str}', y=1.05, fontweight='bold')
plt.xlabel('Impact Category')
plt.ylabel('Liters eq')
    
# Displaying the legend
legend = plt.legend(title='Recipe', loc='upper left', bbox_to_anchor=(1, 1))
legend.get_frame().set_facecolor('none')

# Saving the plot
plt.savefig(os.path.join(save_path_impacts, f'stacked_bar_Str_{highest_impact_recipe_str}.png'), bbox_inches='tight')

# Showing the plot
plt.show()

#%%