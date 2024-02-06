import pandas as pd

#%%
df1 = pd.read_excel('aaq0216_datas2.xls', sheet_name='Results - Global Totals')
 
print(df1)
# %%
#Substracting the data needed
df2 = df1.iloc[1:56, 0:16]

print(df2)
# %%
# ** CLEANING DATASET
# Change the name of some columns
df3 = (
    df2.rename(columns={'Unnamed: 0':'Food group', 'Unnamed: 1': 'Food and Waste', 'Impact / kg Food Balance Sheet functional unit (ex. waste)': 'Land Use (m2) Arable',
                                  'Unnamed: 3': 'Land Use (m2) Fallow',
                                  'Unnamed: 4': 'Land Use (m2) Perm Past',
                                  'Unnamed: 5':'GHG (kg CO2eq, IPCC 2013) LUC',
                                  'Unnamed: 6':'GHG (kg CO2eq, IPCC 2013) Feed',
                                  'Unnamed: 7':'GHG (kg CO2eq, IPCC 2013) Farm',
                                  'Unnamed: 8':'GHG (kg CO2eq, IPCC 2013) Processing',
                                  'Unnamed: 9':'GHG (kg CO2eq, IPCC 2013) Transport',
                                  'Unnamed: 10':'GHG (kg CO2eq, IPCC 2013) Packging',
                                  'Unnamed: 11':'GHG (kg CO2eq, IPCC 2013) Retail',
                                  'Unnamed: 12':'Acid.(kg SO2eq)',
                                  'Unnamed: 13':'Eutr. (kg PO43-eq)',
                                  'Unnamed: 14':'Freshwater (L)',
                                  'Unnamed: 15':'Str-Wt WU (L eq)'})
)

print(df3)
#%%
#Removing the second row
#df4 = df3.drop(['Product'])
df4 = df3.iloc[1:,:]
print(df4)
#%%
#Dropping if all values in the row are nan
df4 = df3.dropna(how='all') 

print (df4)
#%%
#Checking some values
print(df4['Acid.(kg SO2eq)'].loc[df4.index[10]])
