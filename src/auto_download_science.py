"""
THIS IS NOT WORKING.

Issue: Science.org is blocking requests from scripts.
Tried to use headers to make it look like a browser request, but still not working.
Current browser send more complex headers than this script. 
But as this only an one-time download, I will not spend more time on this.
"""


#%%
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

dls = "https://www.science.org/doi/suppl/10.1126/science.aaq0216/suppl_file/aaq0216_datas2.xls"
resp = requests.get(dls, headers=headers)
resp.raise_for_status()    # Check that the request was successful

output = open('test.xls', 'wb')
output.write(resp.content)
output.close()
