# Thesis Spring 2024

This repository contains the work for the thesis in Spring 2024 regarding the Recipe calculator.

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

1. constants.py - this file contains the different constants used in the project
2. ProjectFunctions.py - this file contains the functions to read the different datasources and files
3. cleaning.py - this file contains the code to clean the Poore & Nemecek database, this database has all the impacts per food group
4. analyze_data.py - this file contains the code to improve the Poore & Nemecek database resolution and the calculation of the recipe's impacts.

### ./data

There are two folders indicating the level of transformation of the data

1. raw - it contains the origial Poore & Nemecek database downloaded from the academic article website
2. interim - it contains all the other databases that are either saved from the code or created to be merged with other databases.
    2.1. Clean_Poore&Nemecek = this is the database obtained from the cleaning.py file
    2.2. Conversion_factors = this file contains the conversion factors from units like tbsp, tsp, cup, and so on into grams
    2.3. Fooditem_PooreNemecek = this file is obtained after merging the ingredient_foodgroup file and Clean_Poore&Nemecek in order to add the food items to the original impact database
    2.4. Recipe_template = the user needs to download this template and fill out the amounts for each ingredient that is part of the recipe, and specify the unit, if it is unit, grams, tbsp, tsp, cup, bunch, etc. Then, save the document in this folder again without changing the name of the file
    2.5. ingredient_foodgroup = this file allows to increase the resolution of the Poore&Nemecek database regarding the food item detail