import requests
from bs4 import BeautifulSoup

def search_torrents(query):
    url = f"https://1337x.to/search/{query}/1/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for row in soup.select("tr")[1:6]:  # top 5 results
        name = row.select_one("td.coll-1").text
        link = "https://1337x.to" + row.select_one("td.coll-1 a")["href"]
        magnet = get_magnet(link)
        results.append({"name": name, "magnet": magnet})
    return results

def get_magnet(detail_url):
    res = requests.get(detail_url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.select_one("a[href^=magnet:]")["href"]
