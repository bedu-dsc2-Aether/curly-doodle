import requests
import pandas as pd
from pprint import pprint as pp

url = 'https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML'
html = requests.get(url).content
table_list = pd.read_html(html, skiprows=1) # Headers are correct but the first row (Label, question, section, etc) is missing
layout_df = table_list[-1]
for table in table_list[:5]:
    pp(table.head())