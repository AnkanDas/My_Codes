import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import NoSuchElementException
import csv
import xlrd
import requests
import re
import xlwt
import pygal
import plotly.offline as offline

f1 = xlrd.open_workbook("/Users/Ankan/Documents/Cleaning Data from diff sources/GraphsforB2B_Pygal.xlsx")


'''
YoY-Trend
'''
reader1 = f1.sheet_by_name("yoy")
print(reader1.cell(0,0))

# line_chart.title = reader1.cell(0,0)
xaxis = []
yaxis = ["Deals","Amount"]
deals = []
amount = []
for i in range(2,5):
    xaxis.append(int(reader1.cell_value(i,0)))
    deals.append(int(reader1.cell_value(i, 1)))
    amount.append(int(reader1.cell_value(i, 2)))

print(xaxis)
print(deals)
print(amount)

line_chart = pygal.Line(secondary_range=(min(amount), (max(amount)+10000000)))
line_chart.x_labels = xaxis
line_chart.add(yaxis[0],deals)
line_chart.add(yaxis[1],amount,secondary=True)
line_chart.render_to_file('/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/yoy.svg')


'''
QoQ-Trend
'''
reader1 = f1.sheet_by_name("yoy")
print(reader1.cell(0,0))

# line_chart.title = reader1.cell(0,0)
xaxis = []
yaxis = ["Deals","Amount"]
deals = []
amount = []
for i in range(9,17):
    xaxis.append(str(reader1.cell_value(i,0)))
    deals.append(int(reader1.cell_value(i, 1)))
    amount.append(int(reader1.cell_value(i, 2)))

print(xaxis)
print(deals)
print(amount)

line_chart = pygal.Line(secondary_range=(min(amount), (max(amount)+10000000)))
line_chart.x_labels = xaxis
line_chart.add(yaxis[0],deals)
line_chart.add(yaxis[1],amount,secondary=True)
line_chart.render_to_file('/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/QoQ.svg')


'''
Location-Trend
Amount is dot chart, Deals in Rader chart
'''
reader1 = f1.sheet_by_name("location")
print(reader1.cell(0,0))

xaxis = ["2014","2015","2016"]
yaxis = []
rowit = []
amount = []
deals = []
for i in range(1,8):
    yaxis.append(str(reader1.cell_value(i,0)))
    for j in range(1,4):
        rowit.append(int(reader1.cell_value(i,j)))
    amount.append(rowit)
    rowit = []
    for j in range(4,7):
        rowit.append(int(reader1.cell_value(i, j)))
    deals.append(rowit)
    rowit = []

dealsexp = []
a = []
for i in range(4,7):
    for j in range(1,8):
        a.append(int(reader1.cell_value(j, i)))
    dealsexp.append(a)
    a = []


print(yaxis)
print(xaxis)
print(deals)
print(amount)
print(dealsexp)

dot_chart1 = pygal.Dot()
dot_chart2 = pygal.Radar()
dot_chart1.title = 'CityWise Amount'
dot_chart2.title = 'CityWise Deals'
dot_chart1.x_labels = xaxis
dot_chart2.x_labels = yaxis

for i in range(0,6):
    dot_chart1.add(yaxis[i],amount[i])

for i in range(0,3):
    dot_chart2.add(xaxis[i],dealsexp[i])


dot_chart1.render_to_file('/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/location_a.svg')
dot_chart2.render_to_file('/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/location_d.svg')

'''
Status Pie
'''
reader1 = f1.sheet_by_name("status")
print(reader1.cell(0,0))

statustype = []
count = []

for i in range(1,5):
    statustype.append(str(reader1.cell_value(i,0)))
    count.append(int(reader1.cell_value(i, 1)))

pie_chart = pygal.Pie(inner_radius=0.6)
pie_chart.title = 'Status of Startups funded in 2014 - 2016'
for i in range(0,4):
    pie_chart.add(statustype[i],count[i])

pie_chart.render_to_file('/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/status.svg')

'''
Location-Trend
Amount & Deals in Scatter
'''
reader1 = f1.sheet_by_name("location")
print(reader1.cell(0,0))

city = []
dealamt = []
buf = []
for i in range(13,20):
    city.append(reader1.cell_value(i, 0))
    for j in range(1,4):
        c = reader1.cell_value(i,j)
        c = c.strip('()\n').split(',')
        buf.append(tuple(float(x) for x in c))
    dealamt.append(buf)
    buf=[]

print(dealamt)

xy_chart = pygal.XY(stroke=False)
xy_chart.title = 'City'

for i in range(0,6):
    xy_chart.add(city[i],dealamt[i])

xy_chart.render_to_file("/Users/Ankan/Documents/Cleaning Data from diff sources/B2B_Pygal_Graphs/location_s.svg")