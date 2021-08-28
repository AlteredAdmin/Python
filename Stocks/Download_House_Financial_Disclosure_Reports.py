# Title: Python - Download House Financial Pdfs
# Description: Downloads Financial Disclosure Reports from disclosures-clerk.house.gov
# More info: https://alteredadmin.github.io//posts/python-download-house-financial-pdfs/
# =====================================================
# Name: Altered Admin
# Website: https://alteredadmin.github.io/
# If you found this helpful Please consider:
# Buymeacoffee: http://buymeacoffee.com/alteredadmin
# BTC: bc1qhkw7kv9dtdk8xwvetreya2evjqtxn06cghyxt7
# LTC: ltc1q2mrh9s8sgmh8h5jtra3gqxuhvy04vuagpm3dk9
# ETH: 0xef053b0d936746Df00C9CCe0454b7b8afb1497ac

import datetime
import wget
import pandas as pd
from zipfile import ZipFile
from xmlutils.xml2csv import xml2csv
import os.path
from pathlib import Path
from os.path import expanduser

now = datetime.datetime.now()
year = now.year
fdurl = ('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/' + str(year) + 'FD.ZIP')
fdzip = str(year) + 'FD.ZIP'
fdxml = str(year) + 'FD.xml'
fd = 'FilingDate'
docD = os.path.join(os.environ.get("HOME"), 'TheHouse')

print()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)
print()

print('Downloading ' + fdzip)
print(fdzip)
wget.download(fdurl)
print('Extracting XML File...')
print()
with ZipFile(fdzip, 'r') as zipObj:
    listOfFileNames = zipObj.namelist()
    for fileName in listOfFileNames:
        if fileName.endswith('.xml'):
            zipObj.extract(fileName)

print('Converting to CSV....')
print()
converter = xml2csv(fdxml, "FDHouse.csv", encoding="utf-8")
converter.convert(tag="Member")

print("Getting last 10 days & sorting list...")
print()
df = pd.read_csv('FDHouse.csv')
df[fd] = pd.to_datetime(df[fd])
mask = df[fd] >= (pd.to_datetime('now') - pd.DateOffset(days=40))
df[mask].to_csv('lastdays.csv', index=False)

df = pd.read_csv('lastdays.csv')
df[fd] = pd.to_datetime(df[fd])
sortedlist = df.sort_values(by=["FilingDate"], ascending=False)
sortedlist.to_csv('sortedlastdays.csv', index=False)
print(sortedlist)
print()

print('Getting DocIDs...')
print()
docids = []
data = pd.read_csv('sortedlastdays.csv')
for v in data['DocID']:
    # print(v)
    docids.append(v)
for ids in docids:
    home = expanduser("~")
    folder = os.path.join(os.environ.get("HOME"), 'THeHouse', '')
    # print(folder)
    pdf = (folder + str(ids) + '.pdf')
    # print(pdf)
    if Path(pdf).is_file():
        print()
        print("PDF " + str(ids) + " exist")
        print()
    else:
        try:
            wg = wget.download('https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/' + str(ids) + '.pdf', docD)
            print()
            print('Downloaded: ' + str(ids))
            print(wg)
            print()
        except:
            print()
            print('DocID ' + str(ids) + ' not Found on disclosures-clerk.house.gov')
            print()
            continue

print()
print('Cleaning up files...')
print()
os.remove(fdzip)
os.remove(fdxml)
os.remove("FDHouse.csv")
os.remove("lastdays.csv")
os.remove('sortedlastdays.csv')

print()
print('DONE!!!')
print()
