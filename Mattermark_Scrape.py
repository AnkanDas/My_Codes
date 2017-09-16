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

link = "https://mattermark.com/companies/snapdeal.com"

page = requests.get(link)

#LXMl parser
tree = html.fromstring(page.text)

# Overview: Basic Stats

title = tree.xpath("//h1/a/span/text()")
description = tree.xpath("//p[@class='description']/text()")
tags = tree.xpath("//span/div[@class='pill']/text()")
location = tree.xpath("//div[@class='qf-cell col-xs-6 col-md-4'][1]/p/text()")
founded = tree.xpath("//div[@class='qf-cell col-xs-6 col-md-4'][2]/p/text()")
employee = tree.xpath("//div[@class='qf-cell col-xs-6 col-md-4'][3]/p/text()")
stage = tree.xpath("//div[@class='qf-cell col-xs-6 col-md-4'][4]/p/text()")
totalfunding = tree.xpath("//div[@class='qf-cell col-xs-6 col-md-4'][5]/p/text()")

all_funding = tree.xpath("//div[@class='funding-history']/div[@class='funding']")
all_acq = tree.xpath("//div[@class='acquisitions']/div[@class='acquisition']")

n_funding = len(all_funding)
n_acq = len(all_acq)

# # assign the content of the webpage to soup
soup = BeautifulSoup(page.content, "html.parser")

# print(soup.prettify())

# Variables
qfunding = str()
qacq = str()
famount = []
fstages = []
finvestors = []
fdate = []
acqcompany = []
acqdate = []



funding_history = []
acq_history = []

# creating a tree for the funding data: msoup
a = soup.find_all("div", class_="funding")
for i in a:
    qfunding += str(i)

msoup = BeautifulSoup(qfunding, "lxml")
print(msoup)

# Get amount and stage from msoup
b = msoup.find_all("h3")
print (b)

# Get investor list from msoup
c = msoup.find_all("p")
print(c)

# Get date of funding from msoup
d = msoup.find_all("div", class_="data-label")
print (d)


for i in b:
    x = i.text
    y = x.split(' ',1)
    famount.append(y[0])
    fstages.append(y[1])
    print (y)

for i in c:
    x = i.text
    y = x.split(',')
    print(y)
    finvestors.append(y)

for i in d:
    x = i.text.strip()
    print(x)
    fdate.append(x)

# creating a tree for the M&A data: asoup

a = soup.find_all("div", class_="acquisition")
for i in a:
    qacq += str(i)

asoup = BeautifulSoup(qacq, "lxml")
# print(asoup)

# Get amount and stage from msoup
b = asoup.find_all("h3")
print (b)

# Get date of funding from msoup
d = asoup.find_all("div", class_="data-label")
print (d)

for i in b:
    acqcompany.append(i.text)

for i in d:
    acqdate.append(i.text)



# print (fdate)
# print (famount)
# print (fstages)
# print (finvestors)
print (n_funding)



# i = 0
for i in range(0,n_funding):
    try:
        dummy = []
        dummy.append(fdate[i])
        dummy.append(famount[i])
        dummy.append(fstages[i])
        dummy.append(finvestors[i])
        funding_history.append(dummy)
        # i +=1
    except IndexError:
        pass


# i = 0
for i in range(0,n_acq):
    dummy = []
    dummy.append(acqdate[i])
    dummy.append(acqcompany[i])
    acq_history.append(dummy)
    # i += 1


# Geting social links
social = []
for h in soup.select("span.social-icons [href]"):
    social.append(h['href'])


# Getting Social Stats: tw
tw = []
twitterhandle = tree.xpath('//*[@id="social-container"]/div/div/div/div[1]/div[1]/div/div[1]/p/a/@href')
# print (twitterhandle)
tw.append(twitterhandle)
twitterfollow = tree.xpath("//div[@class='tab-pane fade active in']/div[@class='container-fluid']/div[@class='row']/div[@class='col-md-4 col-xs-12'][2]/p/text()")
# print (twitterfollow)
tw.append(twitterfollow)
twittermentions = tree.xpath("//div[@class='tab-pane fade active in']/div[@class='container-fluid']/div[@class='row']/div[@class='col-md-4 col-xs-12'][3]/p/text()")
# print (twittermentions)
tw.append(twittermentions)


# Getting Social Stats: fb
fb = []
fbhandle = tree.xpath("//*[@id='social-container']/div/div/div/div[2]/div[1]/div/div[1]/p/a/@href")
# print (fbhandle)
fb.append(fbhandle)
fbfollow = tree.xpath("//*[@id='social-container']/div/div/div/div[2]/div[1]/div/div[2]/p/text()")
# print (fbfollow)
fb.append(fbfollow)

# Getting Social Stats: ln
ln = []
lnhandle = tree.xpath("//*[@id='social-container']/div/div/div/div[3]/div[1]/div/div[1]/p/a/@href")
# print (lnhandle)
ln.append(lnhandle)
lnfollow = tree.xpath("//*[@id='social-container']/div/div/div/div[3]/div[1]/div/div[2]/p/text()")
# print (lnfollow)
ln.append(lnfollow)

socialstats = []
socialstats.append(tw)
socialstats.append(fb)
socialstats.append(ln)


# Key People

allpersons = []
for i in range(1,len(soup.find_all("div", class_="person"))):
    oneperson = []
    pername = tree.xpath("//div[@class='person'][{}]/span[@class='p-name']/a/span/text()".format(i))
    pertile = tree.xpath("//div[@class='person'][{}]/span[@class='p-title']/text()".format(i))
    perurl = tree.xpath("//*[@id='webapp']/div/div[2]/div[3]/div[2]/div[1]/div[{}]/span[1]/a/@href".format(i+1))
    oneperson.append(pername)
    oneperson.append(pertile)
    oneperson.append(perurl)
    allpersons.append(oneperson)

# Values
print (title)
print (description)
print (tags)
print (location)
print (founded)
print (employee)
print (stage)
print (totalfunding)
print (funding_history)
print (acq_history)
print (social)
print (socialstats)
print (allpersons)

rowdata = []
rowdata.append(title)
rowdata.append(description)
rowdata.append(tags)
rowdata.append(location)
rowdata.append(founded)
rowdata.append(employee)
rowdata.append(stage)
rowdata.append(totalfunding)
rowdata.append(funding_history)
rowdata.append(acq_history)
rowdata.append(social)
rowdata.append(socialstats)
rowdata.append(allpersons)
rowdata.append(link)


header = ["Name","Description","Markets","Location","Founding Year","Employee Count","Stage","total funding","Funding History","Acqusitions","Social links","Social Stats","Key People"]

with open('/Users/Ankan/Documents/Company_Mattermark_Scrape.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(rowdata)