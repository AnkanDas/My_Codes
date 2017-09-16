import xlrd
import nltk
import csv
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from stopwords import get_stopwords
from nltk.stem.porter import PorterStemmer
import re
import sys
import ast
import ngram

# wb = xlrd.open_workbook('/Users/Ankan/Documents/Data For Nucleus/NB_Tags.xlsx')
# ws1 = wb.sheet_by_name('Sheet1')
# ws2 = wb.sheet_by_name('Sheet2')
#
# for i in range(0,ws2.nrows):
#     prob = []
#     mydict = {}
#     for j in range(1, ws1.nrows):
#         temp = {}
#         comp = ngram.NGram.compare(ws1.cell_value(j,4),ws2.cell_value(i,4))
#         prob.append(comp)
#         key = ws1.cell_value(j,1)
#         temp[key] = comp
#         mydict.update(temp)
#     maxim = max(prob)
#     print ((list(mydict.keys())[list(mydict.values()).index(maxim)]))


wb = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Others/did_not_scrape_MM.xlsx')
ws = wb.sheet_by_name('Sheet1')


with open('/Users/Ankan/Documents/Data For Nucleus/links_MM.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

for i in range(0,ws.nrows):
    line = ws.row(i)
    with open('/Users/Ankan/Documents/Data For Nucleus/links_MM.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(ws.row_values(i))


