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
import pandas as pd


data = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/FundingReport_OuterJoin_nucleus42data.xlsx',
                     sheetname="outer_join")


# print (data.columns.values.tolist())

# print (data[["Startup Name","F_Date"]])

unique_names = data["Startup Name"].str.lower().unique()
# for x in unique_names:
#     print (x)
print (len(unique_names))

# for i in range(0,len(data["Startup Name"])):
#     for name in unique_names:
#         print(data.where(data["Startup Name"].str.lower()==name))





# writer = pd.ExcelWriter("/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/new_db.xlsx")
# finaldata.to_excel(writer,'inc42data')
# writer.save()