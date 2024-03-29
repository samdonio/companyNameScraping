import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os
from tldextract import extract
#if you get 88640 code turn on VPN

start = time.time()
df = pd.read_csv("public_150k_plus_230101.csv") #check name of csv from where data is being read
outdf = pd.DataFrame(columns=["Business Name", "URL"])
filterout = ["dnb", "facebook", "linkedin", "bbb", "buildzoom","yelp","bloomberg","imdb","indeed","glassdoor","youtube",".gov"] #list of websites/keywords to filter out

results = 1 #can select how many google search results to return / not working 100%
lower = 0 #lower index from data.csv to search **CHANGE ME**
upper = 100000 #upper index **CHANGE ME*

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

for i in range(lower, upper):
    tdf = df.iloc[i, [4, 5, 6, 7, 8]]
    busName = tdf[0] #Additional info of company
    Addy = tdf[1]
    City = tdf[2]
    State = tdf[3]
    Zipcode = tdf[4]
    if str(City) == "nan":
        query = str(busName)
    else:
        query = str(busName)+ "+" +str(City)
    search = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={search}&ie=utf-8&oe=utf-8"
    try:
        requests_results = requests.get(url)
        soup_link = BeautifulSoup(requests_results.content, "html.parser")
        up = False
        links = soup_link.find_all("a")
        if '86640' in str(links): #google too many request code
            print('86640 error index ' + str(i))
            outdf.loc[len(outdf.index)] = [busName, '86640 error']
            break
        else:
            for link in links:
                if up == False:
                    link_href = link.get("href")
                    if "url?q=" in link_href and not "webcache" in link_href:
                        title = link.find_all("h3")
                        if len(title) > 0:
                            s = link.get("href").split("?q=")[1].split("&sa=U")[0]
                            rem = False
                            up = False
                            for j in filterout:
                                if j in s:
                                    rem = True
                            if rem == False:
                                ext = extract(s)
                                s = ext.registered_domain
                                up = True
                                outdf.loc[len(outdf.index)] = [busName, s.replace("/", "")]
            if up == False:
                outdf.loc[len(outdf.index)] = [busName, 'x']
    except requests.exceptions.Timeout:
        print('Timeout occurred index '+ str(i))
        outdf.loc[len(outdf.index)] = [busName, 'timeout']
        break
    try:
        os.remove('PPP_File1_Index('+str(lower)+'-'+str(len(outdf)+lower-1)+').csv')
    except:
        pass
    finally:
        outdf.to_csv('PPP_File1_Index('+str(lower)+'-'+str(len(outdf)+lower)+').csv') #name of export csv
        print(i)
print("done")
print(time.time() - start)
