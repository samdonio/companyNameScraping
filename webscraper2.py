import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from time import sleep


def nameToWebsite(name="", state=""):

    noSpaceName = name.replace(" ", "+")

    noSpaceState = state.replace(" ", "+")

    

    toSearch = noSpaceName + "+" + noSpaceState

    

    requestName = "https://google.com/search?q=" + toSearch

    print(f"Searching for {name + '' + state}")

    request = urllib.request.Request(requestName)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()

    html = raw_response.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all('a'):
        if link.get('href') and \
        "google" not in link.get('href') and \
        "search" not in link.get('href') and \
            link.get('href') != '#':
            # sleep(2)
            return link.get('href')



df = pd.read_csv("public_150k_plus_230101.csv")

dfSubset = df.head(25)

dfSubset = dfSubset[["BorrowerName", "BorrowerCity"]].fillna("")

dfSubset["website"] = dfSubset.apply(lambda x: nameToWebsite(x.BorrowerName, x.BorrowerCity), axis=1)


print(dfSubset)