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

wb1 = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Inc42CMS/Funding Data/Indian Funding Data/Funding Report 2017 H1/Tagged Investors.xlsx')
ws1 = wb1.sheet_by_name('Sheet3')

wb2 = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Inc42CMS/Funding Data/Indian Funding Data/Q12015_Q22017_Indian_Startup_Funding_Data.xlsx')
ws2 = wb2.sheet_by_name('Funding 2015 - 2017q2')

investor_count = []
for i in range(1,ws2.nrows):
    temp = []
    investors = ws2.cell_value(i,10)
    startupname = ws2.cell_value(i,5)
    # print (investors)
    counter = 0
    for i in range(1,ws1.nrows):
        if ws1.cell_value(i,2) == "Venture Capital":
            investor = ws1.cell_value(i,0)
            if investor in investors:
                print (investor)
                counter +=1
    temp.append(startupname)
    temp.append(investors)
    temp.append(len(investors.split(",")))
    temp.append(counter)
    investor_count.append(temp)
    print(investors)
    print(counter)

print (investor_count)

with open('/Users/Ankan/Documents/Data For Nucleus/investorcount.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(["Investors","VC count"])

for i in range(0,(len(investor_count)-1)):
    # line = ws.row(i)
    with open('/Users/Ankan/Documents/Data For Nucleus/investorcount.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(investor_count[i])