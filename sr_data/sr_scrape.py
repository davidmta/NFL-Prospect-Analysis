import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv

def parse_year(tr):
    year = re.search('\>\d+\<\/a\>',str(tr))
    return strip_raw(year.group(0))

def strip_conference(raw_conference):
    left = raw_conference.find('>')
    right = raw_conference.find('<')
    return raw_conference[left+1:right]

def conference_search(def_stats_entry,tr):
    raw_conference = re.search('conferences/\w+/\d+\.html\"\>\w+\<\/a\>\<\/',str(tr))
    conference = strip_conference(raw_conference.group(0))
    def_stats_entry.append(conference)
    return def_stats_entry

def class_search(def_stats_entry, tr):
    return def_stats_entry

def parse_defense(tr,def_stats):
    year = parse_year(tr)
    def_stats_entry = []
    def_stats_entry = conference_search(def_stats_entry,tr)
    def_stats_entry = class_search(def_stats_entry, tr)
    return def_stats;

def player_stats(player_url,years_active,player_name,categories):
    print "https://www.sports-reference.com" + player_url
    page = requests.get("https://www.sports-reference.com" + player_url)
    soup = BeautifulSoup(page.content,"html.parser")
    tr_soup = soup.findAll('tr')
    def_stats = {}
    for tr in tr_soup:
        stat_box_result = re.search('\<a href\=\"\/cfb\/years\/\d+\.html\"\>\d+\<\/a\>',str(tr))
        if stat_box_result != None:
            if re.search('tackles_assists',str(tr)) != None:
                def_stats = parse_defense(tr,def_stats)
    sys.exit(1)

### school = re.sub("[^a-zA-Z]+", "", raw_school.group(0))
def strip_raw(raw):
    return raw[1:len(raw)-4]

def strip_raw_url(raw_url):
    return raw_url[12:]

def get_players(page,categories):
    soup = BeautifulSoup(page.content,"html.parser")
    p_soup = soup.findAll('p')
    for p in p_soup:
        url_result = re.search('\<p\>\<a href\=\"/cfb/players/\w+\-\w+\-\d.html',str(p))
        years_result = re.search('\(\d+\-\d+\)',str(p))
        name_result = re.search('\>\w+ \w+\<\/a\>',str(p))
        if url_result and years_result and name_result != None:
            years_active = years_result.group(0)
            player_url = strip_raw_url(url_result.group(0))
            player_name = strip_raw(name_result.group(0))
            player_stats(player_url,years_active,player_name,categories)
    return players


def get_data(categories):
    for letter in range(ord('a'),ord('b')):
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter)+"-index.html")
        get_players(page,categories)
        page_index = 2
#        while(True):
#            page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index-" + str(page_index) + ".html")
#            if page.status_code == 404:
#                return
#            page_index = page_index + 1

def create_CSV(categories):
    sr_cfb_database = open('sr_cfb_database.csv', 'w')
    with sr_cfb_database:
        writer = csv.writer(sr_cfb_database)
        writer.writerows(categories)

def main():
    categories = [["PLAYER","COLLEGE","YEARS ACTIVE","POSITION","HEIGHT","WEIGHT","DRAFT","PASSING", "RUSHING AND RECEIVING", "PUNTING AND KICKING","DEFENSE AND FUMBLES","SCORING","PUNT AND KICK RETURNS"]]
    create_CSV(categories)
    get_data(categories)
    return 0;

if __name__ == "__main__":
    main()
