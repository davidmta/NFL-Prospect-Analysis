import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv

def parse_year(text):
    year = re.search('\>\d+\<\/a\>',text)
    return strip_raw(year.group(0))

def strip_raw_info(raw_conference):
    left = raw_conference.find('>')
    right = raw_conference.find('<')
    return raw_conference[left+1:right]

def stats_search(pattern,def_stats_entry,tr):
    raw_info = re.search(pattern,tr)
    if raw_info == None:
        def_stats_entry.append('')
    else:
        conference = strip_raw_info(raw_info.group(0))
        def_stats_entry.append(conference)
    return def_stats_entry

def parse_defense(tr,def_stats):
    year = int(parse_year(tr))
    def_stats_entry = []
    ## Conference
    def_stats_entry = stats_search('href\=\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a\>\<\/td\>',def_stats_entry,tr)
    ## Class
    def_stats_entry = stats_search('\"class\"\s\>\w+\<\/td\>',def_stats_entry,tr)
    ## Position Played
    def_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',def_stats_entry,tr)
    ## Games
    def_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Solo Tackles
    def_stats_entry = stats_search('\"tackles\_solo\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Assisted Tackles
    def_stats_entry = stats_search('\"tackles\_assists\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Total Tackles
    def_stats_entry = stats_search('\"tackles\_total\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Tackles For Losses
    def_stats_entry = stats_search('\"tackles\_loss\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Sacks
    def_stats_entry = stats_search('\"sacks\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Interceptions
    def_stats_entry = stats_search('\"def\_int\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Interceptions Yards
    def_stats_entry = stats_search('\"def\_int\_yds\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Interception Return Yards Per Interception
    def_stats_entry = stats_search('\"def\_int\_yds\_per\_int\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Interception Touchdowns
    def_stats_entry = stats_search('\"def\_int\_td\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Passes Defensed
    def_stats_entry = stats_search('\"pass\_defended\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Recovered
    def_stats_entry = stats_search('\"fumbles\_rec\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Recovery Return Yards
    def_stats_entry = stats_search('\"fumbles\_rec\_yds\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumble Recovery Return Touchdowns
    def_stats_entry = stats_search('\"fumbles\_rec\_td\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Forced
    def_stats_entry = stats_search('\"fumbles\_forced\"\s\>\d+\<\/td',def_stats_entry,tr)
    def_stats[year] = def_stats_entry
    return def_stats;

def parse_passing(tr,pass_stats):
    year = int(parse_year(tr))
    pass_stats_entry = []
    ## School
    pass_stats_entry = stats_search('\"\/cfb\/schools\/\w+\/\d+\.html\"\>\w+\<\/a',pass_stats_entry,tr)
    ## Conferences
    pass_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',pass_stats_entry,tr)
    ## Class
    pass_stats_entry = stats_search('class\"\s\>\w+\<\/',pass_stats_entry,tr)
    ## Position Played
    pass_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',pass_stats_entry,tr)
    ## Games
    pass_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Completions
    pass_stats_entry = stats_search('\"pass\_cmp\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Attempts
    pass_stats_entry = stats_search('\"pass\_att\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Completion Percentage
    pass_stats_entry = stats_search('\"pass\_cmp\_pct\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Passing Yards
    pass_stats_entry = stats_search('\"pass\_yds\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Yards Per Attempt
    pass_stats_entry = stats_search('\"pass\_yds\_per\_att\"\s\>d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Adjusted Passing Yards Per Attempt
    pass_stats_entry = stats_search('\"adj\_pass\_yds\_per\_att\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Passing Touchdowns
    pass_stats_entry = stats_search('\"pass\_td\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Interceptions
    pass_stats_entry = stats_search('\"pass\_int\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Efficency Rating
    pass_stats_entry = stats_search('\"pass\_rating\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    pass_stats[year] = pass_stats_entry
    return pass_stats;

def player_stats(player_url,years_active,player_name,categories):
    page = requests.get("https://www.sports-reference.com" + player_url)
    pass_stats = def_stats = {}
    trs = re.findall('\<tr\s\>.*?\<\/tr\>',page.content)
    for tr in trs:
        if re.search('tackles_assists',tr) != None:
            def_stats = parse_defense(tr,def_stats)
        elif re.search('pass_att',tr) != None:
            pass_stats = parse_passing(tr,pass_stats)
            print pass_stats


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
            #player_stats(player_url,years_active,player_name,categories)
            player_stats("/cfb/players/andrew-luck-1.html",years_active,player_name,categories)
            sys.exit(1)
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
