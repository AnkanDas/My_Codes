import requests
from bs4 import BeautifulSoup


link = "https://yourstory.com/"

# request to access webpage
page = requests.get(link)

# assign the content of the webpage to soup
soup = BeautifulSoup(page.content, "html.parser")

print(soup)

print(str(soup.find("title-small bentonCondensed bold color-black-2 truncate-3 mt-15")))
raw_text = str()
# for hit in soup.findAll("div class"):
#     raw_text+=str(hit)

print(raw_text)