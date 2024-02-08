from urllib.request import urlopen
from unicodedata import normalize
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd

codebook_df = pd.DataFrame()

url = 'https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML'
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
html_tables = soup.findAll('table',{'class': 'table'})

rows = []
for table in html_tables[1:]:
    attributes_html = table.find('td')
    for br in attributes_html.find_all('br'):
        br.replace_with('\n')

    attributes = normalize('NFKD',attributes_html.text)
    
    d = dict()
    for line in attributes.splitlines():
        k = str(line.split(':')[0]).strip()
        v = str(line.split(':')[1]).strip()
        d[k] = v
    #d = dict(line.split(':') for line in attributes.splitlines())
    attributes_df = pd.DataFrame(d, index=[0])

    table.find('tr').decompose()
    value_catalog_df = pd.read_html(StringIO(str(table)))

    rows.append([attributes_df['SAS Variable Name'],attributes_df,value_catalog_df])

df = pd.DataFrame(rows,columns=['Code', 'Attributes', 'Catalog'])

df.head()