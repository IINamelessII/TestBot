from bs4 import BeautifulSoup
import requests


def get_memes():
    url = "https://www.reddit.com/r/programmingmemes/"
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
          }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    memes_list = soup.findAll("img", {"class": "_2_tDEnGMLxpM6uOa2kaDB3 media-element"})
    return [item.get("src") for item in memes_list]
