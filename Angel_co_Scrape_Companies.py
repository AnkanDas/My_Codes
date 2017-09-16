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

data = []


def get_data(url, website):

    name = "NA"
    tag = "NA"
    location = "NA"
    investment = ""
    date_of_last_funding = "NA"
    type = "NA"


    print(url, website)

    driver = webdriver.Chrome()

    # setting global wait so that find_x waits for this much of time.
    driver.implicitly_wait(10)

    driver.get(url)

    if driver.find_element_by_xpath("//h1[@class='u-fontSize25 u-fontSize24SmOnly u-fontWeight500']"):
        names = driver.find_element_by_xpath("//h1[@class='u-fontSize25 u-fontSize24SmOnly u-fontWeight500']")
        name = names.text
    else:
        name = "not found"

    try:
        location = driver.find_element_by_xpath("//span[@class='s-vgRight0_5 tag'][2]/a[@class='u-uncoloredLink']").text
    except:
        pass
    # else:
    #     location = "not found"


    if driver.find_elements_by_xpath("//div[@class=' dm77 fud43 _a _jm']/p"):
        tags = driver.find_elements_by_xpath("//div[@class=' dm77 fud43 _a _jm']/p")
        tag = tags[0].text
    else:
        tag = "not found"

    if driver.find_elements_by_xpath("//span[@class='s-vgRight0_5 tag'][1]/a[@class='u-uncoloredLink']"):
        types = driver.find_elements_by_xpath("//span[@class='s-vgRight0_5 tag'][1]/a[@class='u-uncoloredLink']")
        type = types[0].text
    else:
        type = "not found"

    if driver.find_elements_by_xpath("//div[@class='c-inset u-clearfix investment_list profile-module']"):
        investments = driver.find_elements_by_xpath("//div[@class='c-inset u-clearfix investment_list profile-module']")
        for a in range(len(investments)):
            investment+= investments[a].text
            investment += ","
    else:
        stage = "not found"

    # stage = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//li[1]/div/div/div/div/div[@class='type']")))

    # if driver.find_element_by_xpath("//li[1]/div/div/div/div/div[@class='date_display']"):
    #     date_of_last_funding = driver.find_element_by_xpath("//li[1]/div/div/div/div/div[@class='date_display']").text
    # elif driver.find_element_by_xpath("//li/div/div/div/div/div[@class='date_display']"):
    #     date_of_last_funding = driver.find_element_by_xpath("//li/div/div/div/div/div[@class='date_display']").text
    # else:
    #     date_of_last_funding = "not found"
    #
    # a = driver.find_elements_by_xpath("//li/div/div/div/div[@class='raised']")
    # if (len(a)>1):
    #     amount_of_last_funding = a[0].text
    # else:
    #     amount_of_last_funding = a[0].text




    print(name)
    print(tag)
    print(type)
    print(location)
    print(investment)
    # print(date_of_last_funding)
    # print(amount_of_last_funding)

    list = [name,tag,type,location,investment]
    data.append(list)
    #print(data)



f = xlrd.open_workbook("/Users/Ankan/Documents/Scappers/workbook1.xlsx")
reader = f.sheet_by_name("Sheet1")

if __name__=='__main__':
    for row in range(reader.nrows): #reader.nrows
        link = reader.cell(row, 0).value
        print(link)
        try:
            get_data(link, 'angel.co')
        except:
            pass
     #get_data("https://angel.co/globality", 'angel.co')


fl = open('/Users/Ankan/Documents/Scappers/Angel_Cocompanies.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['Name', 'tag', 'Location', 'Stage', 'Last_Date', 'Last_Amount'])  # Header
for values in data:
    print(values)
    writer.writerow(values)

fl.close()