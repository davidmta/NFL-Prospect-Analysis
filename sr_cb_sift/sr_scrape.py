import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def get_data():
    for letter in range(97,123):
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index.html")
        soup = BeautifulSoup(page.content, 'html.parser')
    return 0;

def main():
    get_data()
    return 0;

if __name__ == "__main__":
    main()
