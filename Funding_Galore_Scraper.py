import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import csv
from lxml import html
import lxml.html
from lxml import etree
from lxml.etree import XPath
import xml.etree.ElementTree as et


# date_path = XPath("//span[@class='meta'][2]/span[@class='date']")





links = [ "https://inc42.com/buzz/funding-galore-127/","https://inc42.com/buzz/funding-galore-128/", "https://inc42.com/buzz/funding-galore-129/",
          # "https://inc42.com/buzz/funding-galore-130/","https://inc42.com/buzz/funding-galore-131/","https://inc42.com/buzz/funding-galore-132/",
          # "https://inc42.com/buzz/funding-galore-133/","https://inc42.com/buzz/funding-galore-134/","https://inc42.com/buzz/funding-galore-135/",
          # "https://inc42.com/buzz/funding-galore-136/","https://inc42.com/buzz/funding-galore-137/","https://inc42.com/buzz/funding-galore-138/"
        ]

for link in links:
    '''
    creating the list of words from document
    '''
    #request to access webpage
    page = requests.get(link)
    # page = pages.encode('utf-8')
    #assign the content of the webpage to soup
    # soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    # print (list(soup.children))
    tree = html.fromstring(page.content)
    # tree = etree.parse(link)
    date = tree.xpath("//span[@class='meta'][2]/span[@class='date']")
    companies = tree.xpath("//div[@class='entry-content']")
    for i in date:
        print (i.text.strip())
    for i in tree.findall("div[@class='entry-content']"):
        print (i)

    # print ([type(item) for item in list(soup.children)] )






