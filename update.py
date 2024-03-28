#!/usr/bin/env python

import requests
import pandas as pd
from bs4 import BeautifulSoup

response = requests.get(
    "https://softwarelibre.gob.bo/excepciones/Home/referencias",
    verify=False
)
html = BeautifulSoup(response.text, 'html.parser')
df = pd.DataFrame(
    [[field.get_text().strip() for field in row.select('td')] for row in html.select('tr.gradeA[role="row"]')],
    columns=[field.get_text() for field in html.select('thead th')]
)
df.sort_values('Codigo').to_csv('data.csv', index=False)