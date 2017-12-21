import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def get_data():
    for letter in range(ord('a'),ord('b')):
        #page = requests.get("https://www.sports-reference.com/cfb/players/" + str(letter) + "-index.html")
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        page = requests.get("https://www.sports-reference.com/cfb/players/a-index.html",headers=headers)
        #soup = BeautifulSoup(page.content, 'html.parser')
        #print soup.body.div.div.span
    return 0;

def main():
    get_data()
    return 0;

if __name__ == "__main__":
    main()
