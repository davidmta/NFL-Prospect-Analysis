import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv

def player_stats(player_url):
    page = requests.get("https://www.sports-reference.com" + player_url)
    print page
    sys.exit(1)

def strip_raw_url(raw_url):
    return raw_url[12:]

def get_players(page,players):
    soup = BeautifulSoup(page.content,"html.parser")
    p_soup = soup.findAll('p')
    for p in p_soup:
        result = re.search('\<p\>\<a href\=\"/cfb/players/\w+\-\w+\-\d.html',str(p))
        if result != None:
            player_url = strip_raw_url(result.group(0))
            player_stats(player_url)
    return players


def get_data():
    for letter in range(ord('a'),ord('b')):
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter)+"-index.html")
        get_players(page)
        page_index = 2
#        while(True):
#            page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index-" + str(page_index) + ".html")
#            if page.status_code == 404:
#                return
#            page_index = page_index + 1

def create_CSV():
    categories = [["PLAYERS","COLLEGE","YEARS ACTIVE","POSITION","HEIGHT","WEIGHT","DRAFT","PASSING", "RUSHING AND RECEIVING", "PUNTING AND KICKING","DEFENSE AND FUMBLES","SCORING","PUNT AND KICK RETURNS"]]
    sr_cfb_database = open('sr_cfb_database.csv', 'w')
    with sr_cfb_database:
        writer = csv.writer(sr_cfb_database)
        writer.writerows(categories)

def main():
    create_CSV()
    #get_data()
    return 0;

if __name__ == "__main__":
    main()
