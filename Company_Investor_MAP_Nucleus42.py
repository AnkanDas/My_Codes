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

header = ["Investor Name", "Startup Name", "Startup ID"]



with open('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/Investor_list.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(header)



wb = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/Final__Data_Till_June_2017_F&F.xlsx')
ws = wb.sheet_by_name('Final')

investor_data = []
for i in range(1, ws.nrows):
    cell_data = []
    investor_list = ws.cell_value(i,10).split(",")
    for investor in investor_list:
        temp = []
        print (investor.strip())
        temp.append(investor.strip())
        temp.append(ws.cell_value(i,1))
        temp.append(int(ws.cell_value(i,0)))
        # print (temp)
        cell_data.append(temp)
    investor_data.append(cell_data)

final_list = []

for element in investor_data:
    print (element)
    if element not in final_list:
        final_list.append(element)
print (final_list)


for row in final_list:
    for part in row:
        if part[0]:
            with open('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/Investor_list.csv',
                    'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow(part)
