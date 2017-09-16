import wikipedia
from lxml import etree, html
import xlrd
import nltk
from nltk.tokenize import RegexpTokenizer
from stopwords import get_stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sys
import urllib3
import csv
import codecs
import ast

header = ["Name", "Sector", "Founder"]



with open('/Users/Ankan/Downloads/Sector_Company_Founder_Map.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(header)



wb = xlrd.open_workbook('/Users/Ankan/Downloads/Sector_Company_Founder_Email_Map.xlsx')
ws = wb.sheet_by_name('Sheet1')

# print(ws)
data = []

for i in range(1, ws.nrows):
    rowtemp = []
    print(ws.cell_value(i,2).split(","))
    founderarray = ws.cell_value(i,2).split(",")
    for j in range(0,len(founderarray)):
        temp = []
        print (founderarray[j].strip())
        temp.append(ws.cell_value(i,0))
        temp.append(ws.cell_value(i,3))
        temp.append(founderarray[j].strip())
        rowtemp.append(temp)
        print (temp)
    print (rowtemp)
    data.append(rowtemp)
print (data)

with open('/Users/Ankan/Downloads/Sector_Company_Founder_Map.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        for element in row:
            datawriter.writerow(element)
