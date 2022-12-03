import csv

import requests
from bs4 import BeautifulSoup


r = requests.get('https://bfm.sd.gov/vendor/contactinfo.asp')

r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')

rows = soup.find_all('table')[-1].find_all('tr')[1:]

data = [
    ['agency_code', 'agency_name'],
]

for agency in rows:
    code, abbrev, agency, phone = [x.text.strip() for x in agency.find_all('td')]  # noqa
    data.append([code, agency])

with open('sd-agency-codes.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)
