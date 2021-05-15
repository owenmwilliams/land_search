from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup

context = ssl._create_unverified_context()
url = Request("https://www.landsofamerica.com/Pulaski-County-KY/all-land/no-house/", headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url, context=context)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# a, b, c = soup.find_all("span title")
# print(a, b, c)
# print(soup.find_all('span'))

for i in soup.find_all('span', {'class':'_32f8d'}):
    print(i.get_text().strip())

for i in soup.find_all('span', {'class':'_1a278'}):
    print(i.get_text().strip())

# for i in soup.find_all('span', {'class':'title'}):
#     print(i.get_text().strip())