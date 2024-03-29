#!/usr/bin/env python

import requests
import pandas as pd
from bs4 import BeautifulSoup

response = requests.get(
    "https://softwarelibre.gob.bo/excepciones/Home/referencias",
    verify=False
)
html = BeautifulSoup(response.text, 'html.parser')
columns=[
    field.get_text() 
    for field in html.select('thead th')
    ]

def format_field(field, column):
    if column in ['Informe Tec.', 'Detalle']:
        link = field.select('a')[0]
        if link.get_text() != '':
            return link['href']
        else:
            return None
    else:
        return field.get_text().strip()

df = pd.DataFrame(
    [
        {
            column:format_field(field, column) 
            for field, column 
            in zip(row.select('td'), columns)
        } for row in html.select('tr.gradeA[role="row"]')
    ]
)

for col in ['Codigo', 'Años conformidad']:
    df[col] = df[col].astype(int)

df.sort_values('Codigo').to_csv('data.csv', index=False)