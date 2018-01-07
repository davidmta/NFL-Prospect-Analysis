import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv
import sqlite3 as lite
import os

def get_raw_logsplits(stats_type,player_url):
    url = re.sub('.html','/' + stats_type + '/',player_url)
    page = requests.get("https://www.sports-reference.com" + url)
    if page.status_code == 404:
        return
    soup = BeautifulSoup(page.content,"html.parser")
    return soup.findAll('table')

def attempt_connection():
    try:
        con = lite.connect('sr_players_database.db')
        return con
    except Error as e:
        print(e)

def parse_rawstr(raw_str,pattern):
    str_list = []
    indexes = [(m.start(0), m.end(0)) for m in re.finditer(pattern, raw_str)]
    for i in range(0,len(indexes)):
        index = indexes[i]
        date = raw_str[index[0]+1:index[1]-1]
        if i == len(indexes)-1:
            processed_str = raw_str[index[1]:]
        else:     
            processed_str = raw_str[index[1]:indexes[i+1][0]]
        str_list.append(processed_str)
    return str_list

def sift_split(stat):
    raw_splitstats = re.findall('data-stat=\".*?\">.*?\<',stat)


def cull_splits_table(splits_table):
    str_list = parse_rawstr(str(gamelog_table),"data\-stat\=\"split\_id\" scope\=\"row\"\>\w+<\/th\>")
        # sift_split(stat)

def sift_log(stat):
    ## School
    school = re.search("data-stat\=\"school\_name\"\>.*?\<\/",stat)
    ## Game Location
    game_location = re.search("data\-stat\=\"game\_location\"\>.*?\<\/",stat)
    ## Opponent Name
    opponent_name = re.search("data-stat\=\"opp_name\">.*?\<\/a\>",stat)
    ## Stats
    raw_logstats = re.findall('data-stat=\"\w+\">.*?\<',stat)
    raw_logstats = raw_logstats[3:len(raw_logstats)]
    print raw_logstats

def cull_gamelog_table(gamelog_table):
    str_list = parse_rawstr(str(gamelog_table),"\>\d\d\d\d\-\d\d\-\d\d\<")
    for string in str_list:
        sift_log(string)

def main():
    con = attempt_connection()
    with con:
        cur = con.cursor()
        cur.execute("SELECT URL FROM SR_PLAYERS")
        url_list = cur.fetchall()
        for player_url in url_list:
            # gamelog_table = get_raw_logsplits("gamelog", player_url[0])
            # cull_gamelog_table(gamelog_table)
            splits_table = get_raw_logsplits("splits", player_url[0])
            cull_splits_table(splits_table)
            sys.exit(1)
            #cull_gamelog_table(splits_table)

    return 0;

if __name__ == "__main__":
    main()
