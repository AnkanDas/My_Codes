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
import csv
import sys
import urllib3


# http = urllib3.PoolManager()
# HtmlFile = open("/Users/Ankan/Documents/agritech.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# r = http.request('GET', "/Users/Ankan/Documents/agritech.html")
r = open("/Users/Ankan/Documents/agri_tech.rtf",'r')
# print (tree)
soup = BeautifulSoup(r, "html.parser")
print(soup.prettify())

#Variables - Headers
company_name = []
angel_link = []
website_link = []
s_desc = []
HQ = []
market_tag = []
fstage = []
funding = []
employee = []
equity = []
salary = []


#Getting basic info of Soup
basic = soup.find_all("a", class_="startup-link")

basicli = []
count = 0
for i in basic:
    if count % 2 == 1:
        basicli.append(i)
    count += 1

for a in basicli:
    company_name.append(a.text)
    angel_link.append(a['href'])

#Getting short description
pitch = soup.find_all("div", class_="pitch")

for p in pitch:
    p1 = re.sub(r'[^a-zA-Z0-9 ]', " ", p.text).strip()
    s_desc.append(p1)

#getting website link
for l in soup.select("div.website a[href]"):
    website_link.append(l['href'])

#getting location and markets
mixed = []
for i in soup.select("div.tag a"):
    # print (i.text)
    mixed.append(i.text)

slen = len(mixed)

for i in range(0,slen,2):
    HQ.append(mixed[i])

for i in range(1,slen,2):
    market_tag.append(mixed[i])


# Employee count range
for i in soup.select('div[class="column company_size"]'):
    i1 = re.sub(r'[^a-zA-Z0-9-.W+ ]', " ", i.text).replace("Employees","Count: ").strip()
    # print (i1)
    employee.append(i1)

# Stages
for i in soup.select('div[class="column stage"]'):
    i1 = re.sub(r'[^a-zA-Z0-9-.W+ ]', " ", i.text).replace("Stage","").strip()
    # print (i1)
    fstage.append(i1)


# funding
for i in soup.select('div[class="column raised hidden_column"]'):
    i1 = re.sub(r'[^a-zA-Z0-9-.W+ ]', " ", i.text).replace("Total Raised","").strip()
    # print (i1)
    funding.append(i1)

# salary
for i in soup.select('div[class="column hidden_column hiring_salary"]'):
    i1 = re.sub(r'[^a-zA-Z0-9-.W+ ]', " ", i.text).replace("Salary","").replace(" ","").strip()
    # print (i1)
    salary.append(i1)

# equity
for i in soup.select('div[class="column hidden_column hiring_equity"]'):
    i1 = re.sub(r'[^a-zA-Z0-9-.W+% ]', " ", i.text).replace("Equity","").replace(" ","").strip()
    # print (i1)
    equity.append(i1)

employee.pop(0)
fstage.pop(0)


print (company_name)
print (angel_link)
print (s_desc)
print (website_link)
print (HQ)
print (market_tag)
print (employee)
print (funding)
print (fstage)
print (salary)
print (equity)


header = ["Name","angel.co_link","description","website","location","sectors","employee count","funding amount","stage","Employee Salary range","Equity"]

rowdata = []

for i in range(0,183):
    singlerow = []
    singlerow.append(company_name[i])
    singlerow.append(angel_link[i])
    singlerow.append(s_desc[i])
    singlerow.append(website_link[i])
    singlerow.append(HQ[i])
    singlerow.append(market_tag[i])
    singlerow.append(employee[i])
    singlerow.append(funding[i])
    singlerow.append(fstage[i])
    singlerow.append(salary[i])
    singlerow.append(equity[i])
    rowdata.append(singlerow)

print (rowdata)



with open('/Users/Ankan/Documents/AgriTech_Angel_Scrape.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(header)
    for i in range(0,183):
        datawriter.writerow(rowdata[i])







