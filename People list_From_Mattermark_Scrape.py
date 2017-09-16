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

final = []
with open("/Users/Ankan/Documents/Data For Nucleus/Company_Mattermark_Scrape.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        ar = []
        try:
            l = ast.literal_eval(row[12])
            for i in range(0,(len(l))):
                temp = []
                temp.append(row[0])
                temp.append(l[i])
                ar.append(temp)
            # print (ar)
            final.append(ar)
        except:
            pass

print (len(final))


header = ['Company name','Person name','Designation','Linkedin']
with open('/Users/Ankan/Documents/Data For Nucleus/Company_Mattermark_People.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(header)

for i in final:
    with open('/Users/Ankan/Documents/Data For Nucleus/Company_Mattermark_People.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for p in i:
            datawriter.writerow(p)

