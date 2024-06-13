# Thesis Spring 2024

This repository contains the work for the thesis in Spring 2024 regarding the Recipe calculator. In case that the DELI Calculator package is giving troubles, you can download this version.

## Coding environment

The file environment.yml contains all packages necessary for running the code.
The environment can be created by running the following command in the terminal:

```bash
conda env create -f environment.yml
```

or (recommended if you have mamba installed, its faster)

```bash
mamba env create --file environment.yml
```

After the environment is created, it can be activated by running:

```bash
conda activate foodcalc
```

## Repository structure

./src: Contains all the code for the project
./data: Contains all the data used in the project

### ./src

To read the code, the order to read the different files is as follows:

1.	constants.py: defines constants used throughout the different scripts, mainly related to defining paths to different data directories.
2.	project_functions.py: contains generic functions mostly for reading data sets.
3.	cleaning.py: focuses on cleaning the Poore and Nemecek (2018) database, which contains environmental impact data for various food groups.
4.	harmonize_datasources.py: improves the resolution of the cleaned dataset by merging it with additional details. 
5.	analyze_data.py: includes the conversion to grams, the calculation of the recipe's impacts and the generation of all the different tables needed for the visualizations.
6.	visualizations.py: focuses on creating the different charts to compare recipes and provide the breakdown into ingredients.

In this folder, there is another Python file called “sensitivity_uncertainty.py”. While this part is not part of the DELI Calculator package itself, it plays an important role in the results of this thesis. Running this code is necessary for performing sensitivity and uncertainty analyses on certain values. More details are provided in section 3.2.4.1. and 3.2.4.2. respectively.

### ./data

There are four folders indicating the level of transformation of the data.

1.	raw - it contains the original Poore and Nemecek (2018) database downloaded from the academic article website. The database can be downloaded by following this link: https://www.science.org/doi/10.1126/science.aaq0216 ("Resources" section).
2.	interim - it contains all the other databases that are either saved from the code or created to be merged with other databases.
a.	clean_poore_and_nemecek: this is the database obtained from the cleaning.py file.
b.	conversion_factors: this file contains the conversion factors from units like tbsp, tsp, cup, and so on to grams.
c.	food_item_poore_and_nemecek: this file is obtained after merging the ingredient_foodgroup file and clean_poore_and_nemecek in order to add the food items to the original impact database.
d.	recipe_template: the user has to download this template and fill out the amounts for each ingredient that is part of the recipe, and specify the unit, if it is unit, grams, tbsp, tsp, cup, bunch, etc. Then, save the document in this folder again without changing the name of the file.
e.	ingredient_foodgroup: this file allows to increase the resolution of the Poore and Nemecek (2018) database in terms of food detail.
3.	recipes – it contains the Recipe_template files filled in by the user.
4.	impacts – it contains all the results obtained by the DELI Calculator.

### Code

The specific Python version and Python functions or libraries dependencies for running the DELI Calculator are:

·	Python (version 3.8.13)
·	Pandas (version 1.4.2 or later), for data manipulation and analysis.
·	Pathlib (part of the standard library in Python 3.4 and later), for file system path manipulation.
·	OS (part of the standard library), for interacting with the operating system, in particular for listing files in a directory.
·	Numpy (version 1.22.4 or later), for numerical operations on arrays.
·	Matplotlib.pyplot (version 3.5.3 or later), for creating visualizations.

As mentioned above, the code for the DELI Calculator is made up of six logical sections. Here are the details of the last four sections.

·	cleaning.py: In the cleaning process for the Poore and Nemecek (2018) database, the main steps performed were to subset the necessary data, rename columns for clarity, drop rows with Not a Number (NaN) values and save the cleaned dataset.
·	harmonize_datasources.py: To improve the resolution of the cleaned dataset, a merge was performed between the “fooditem_foodgroup” database, which contains the 528 food items and their corresponding food group based on the Poore and Nemecek (2018) database. Some cleaning was then required, essentially moving the Ingredient column to the beginning of the table. The improved dataset was then saved.
·	analyze_data.py: In order to accurately multiply the amounts entered by the user by their corresponding impacts, a recipe conversion to kilograms was necessary. The code iterates through each Excel file contained in the “./recipes” folder to read the data, filtering and converting units to grams using predefined conversion factors from another database. Once converted, the code merges and cleans the data to ensure unit consistency. 
Next, the cleaned recipe data is merged with the impact data from the Poore and Nemecek (2018) database to perform the impact calculations. This involves multiplying the ingredient quantities by their respective impact factors. Finally, the values are converted from grams to kilograms to ensure that the impact values are appropriately scaled to match the amounts provided in grams. The code then stores the impact data for each ingredient and the total impact for each recipe in separate Excel files.
After completing the previous step and saving all relevant impacts, the code creates and saves the impact labels. It then aggregates the data from all the impact files into a single DataFrame, which is also saved in an Excel file. Additionally, the code concatenates individual ingredient impact files into a single DataFrame and saves it. 
Finally, the code calculates the total impacts for specific categories, such as GHG emissions and land use, and saves the results. These categories are further detailed in the database, broken down into life cycle stages and land types respectively.
·	visualizations.py: Here the code creates four main graphs.
o	Spider web chart: This section creates a spider web chart to visualize the relative environmental performance of recipes. It reads data and processes it to scale values relative to the recipe with the highest impact for each category.
o	Stacked bar chart (per recipe and adding the ingredient breakdown): This section creates stacked bar charts to visualize the distribution of impacts per ingredient for each recipe. It processes the data for each recipe and calculates the percentage contribution of each ingredient.
o	Bar chart and Stacked bar chart (per impact category): This section filters the data for a specific impact category, and a bar chart is created to compare the recipes within that category. Next, the recipe with the highest overall impact is selected, and a stacked bar chart is generated to show the breakdown by ingredients for that recipe. This process is repeated for each of the six impact categories.
