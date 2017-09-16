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

# wb1 = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Final Data Sheet (12-July).xlsx')
# ws1 = wb1.sheet_by_name('Sheet1')
#
# wb2 = xlrd.open_workbook('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Inc42CMS/Funding Data/Indian Funding Data/Q12015_Q22017_Indian_Startup_Funding_Data.xlsx')
# ws2 = wb2.sheet_by_name('Funding 2015 - 2017q2')

nucleus42_data = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Final Data Sheet (12-July)_new.xlsx', sheetname="Sheet1")
inc42_data = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Inc42CMS/Funding Data/Indian Funding Data/2015-2017H1_Data.xlsx', sheetname="Funding 2015 - 2017q2")

print (inc42_data.columns.values)
print (nucleus42_data.columns.values)

new_db1 = pd.merge(inc42_data, nucleus42_data, on=['Startup Name','F_Date'], how='inner')
new_db2 = pd.merge(inc42_data, nucleus42_data, on=['Startup Name','F_Date'], how='outer')

new_db3 = pd.merge(inc42_data, nucleus42_data, on=['Startup Name','F_Date'], how='left')

writer = pd.ExcelWriter("/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/new_db.xlsx")
inc42_data.to_excel(writer,'inc42data')
nucleus42_data.to_excel(writer,'Nucleus42data')
new_db1.to_excel(writer,'inner_join')
new_db2.to_excel(writer,'outer_join')
new_db3.to_excel(writer,'left')
writer.save()
# print (new_db)
