from lxml import etree, html
#from StringIO import StringIO
import requests
import re
import csv

"""
find the list of post links of a particular year
"""
posts_data = []

lastpagecount=34

"""
for page=x, extract all company page url
for company = y, extract social links
"""


for pgno in range(1, lastpagecount+1):
    page_url = "https://www.techinasia.com/startup?page={}".format(pgno)
    response = requests.get(page_url)
    with open('page.html', 'w') as f:
        f.write(response.text)
    doc2 = html.fromstring(response.text)

    p = re.compile(r'((http|https)://www.techinasia.com/companies/\S+)', re.UNICODE)
    # posts_data = []
    #print(p)
    for element, src, link, n in doc2.iterlinks():
        if p.match(link):
            print(link)
data = []
for i in posts_data:
    data.append(list(i))
print(data)


#
# fl = open('/Users/Ankan/Documents/YS_Scrape.csv', 'w')
#
# writer = csv.writer(fl)
# writer.writerow(['Title', 'Link', 'Author','Date']) #Header
# for values in data:
#     writer.writerow(values)
#
# fl.close()