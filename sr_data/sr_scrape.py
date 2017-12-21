import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def get_data():
    for letter in range(ord('a'),ord('b')):
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter)+"-index.html")
        soup = BeautifulSoup(page.content,"html.parser")
        p_soup = soup.findAll('p')
        for i in p_soup:
            print i
        page_index = 2
        while(True):
            page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index-" + str(page_index) + ".html")
            if str(page) == "<Response [404]>":
                    return
            page_index = page_index + 1
    return 0;

def main():
    get_data()
    return 0;

if __name__ == "__main__":
    main()
