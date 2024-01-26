#%%
import requests
dls = "https://www.science.org/doi/suppl/10.1126/science.aaq0216/suppl_file/aaq0216_datas2.xls"
resp = requests.get(dls)

output = open('test.xls', 'wb')
output.write(resp.content)
output.close()
