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

header = ["Name", "Description", "Markets", "Location", "Founding Year", "Employee Count", "Stage", "total funding",
          "Acqusitions", "Social links", "Social Stats", "Key People","Mattermark_link", "last fdate","last famount",
          "last fstage","last round Investors"]



with open('/Users/Ankan/Documents/Company_Mattermark_cleaned.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(header)


finaltable = []
with open("/Users/Ankan/Documents/Data For Nucleus/Company_Mattermark_Scrape.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            l = ast.literal_eval(row[8])
            if len(l)>0:
                for i in range(0,(len(l))):
                    rowdata = []
                    fdata = l[i]
                    for cell in row[0:8]:
                        data = re.sub("[()[\]''{}]+", '', cell)
                        # print(data)
                        rowdata.append(data)
                    for cell in row[9:]:
                        rowdata.append(cell)
                    rowdata +=fdata
                    finaltable.append(rowdata)
                    # print (rowdata)
            else:
                rowdata = []
                for cell in row[0:8]:
                    data = re.sub("[()[\]''{}]+", '', cell)
                    # print(data)
                    rowdata.append(data)
                # rowdata.append(row[8])
                for cell in row[9:]:
                    rowdata.append(cell)
                finaltable.append(rowdata)

        except:
            # print (row)
            pass

# print (finaltable[:10])

for i in finaltable[:10]:
    print (i)



for i in finaltable:
    with open('/Users/Ankan/Documents/Company_Mattermark_cleaned.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(i)