#%%
import pandas as pd
import os
from pathlib import Path

#%%
directory_path = Path("..")
os.getcwd()

# %%
# We Create a function to obatin read datasets
# name --> name of the csv that we want to read
# data_folder --> in which folder it is located
# data_origin --> if necessary, the origin of the dataset
# Type --> when the origin of the dataset is needed, then True, if not just
# type False
def dataset_reader(name, data_folder, type):
    if type is True:
        datasets_path = (
            directory_path
            / "data"
            / data_folder
            / name)
        a = datasets_path
        return(pd.read_excel(a, sheet_name='Results - Global Totals'))
    else:
        datasets_path = (
            directory_path
            / "data"
            / data_folder
            / name)
        a = datasets_path
        return(pd.read_excel(a, sheet_name='Results - Global Totals'))
# %%
