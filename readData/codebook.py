from urllib.request import urlopen
from unicodedata import normalize
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd

value_attributes = {}
value_catalogs = pd.DataFrame()

url = 'https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML'
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
html_tables = soup.findAll('table',{'class': 'table'})

for table in html_tables[1:]:
    attributes_html = table.find('td')
    attributes_text = normalize('NFKD',attributes_html.get_text(separator='\n'))
    d = dict()
    for line in attributes_text.splitlines():
        k = str(line.split(':')[0]).strip()
        v = str(line.split(':')[1]).strip()
        d[k] = v
    
    if 'SAS Variable Name' not in d:
        continue
    
    value_code = d['SAS Variable Name']
    d.pop('SAS Variable Name')
    value_attributes[value_code] = d

    table.find('tr').decompose()
    table.find('colgroup').decompose()
    
    value_catalog_df = pd.read_html(StringIO(str(table)))[0]
    value_catalog_df.set_index('Value',inplace=True)
    value_catalog_df = pd.concat([value_catalog_df], keys=[value_code], names=['Code'])
    value_catalogs = pd.concat([value_catalogs,value_catalog_df])