import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

start = time.time()

df = pd.read_csv('data.csv')

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}

outdf = pd.DataFrame(columns=['Business Name', 'URL'])
for i in range(5):
    tdf = df.iloc[i, [4,5,6,7,8]]
    busName = tdf[0]
    Addy = tdf[1]
    City = tdf[2]
    State = tdf[3]
    Zipcode = tdf[4]
    if str(City) == 'nan':
        query = str(busName)
    else:
        query = str(busName) + ' ' + str(City)
    search = query.replace(' ', '+')
    results = 5
    url = (f"https://www.google.com/search?q={search}&num={results}")
    requests_results = requests.get(url)
    soup_link = BeautifulSoup(requests_results.content, "html.parser")
    links = soup_link.find_all("a")
    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
          title = link.find_all('h3')
          if len(title) > 0:
              s = link.get('href').split("?q=")[1].split("&sa=U")[0]
              if 'https://www.' in str(s):
                  print(s.replace('https://www.',''))
              elif 'http://www.' in str(s):
                  print(s.replace('http://www.',''))
              elif 'https://' in str(s):
                  print(s.replace('https://',''))
              else:
                    print(s.replace('http://',''))
    print("------")

print('done')
print(time.time() - start)


