import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv
import sqlite3 as lite
import os
from stats_scrape import strip_raw_info,bracketstrip,strip_quotes,sift_log,sift_split,standardize_for_SQL


def attempt_connection():
    try:
        con = lite.connect('sr_players_database.db')
        return con
    except Error as e:
        print(e)

def get_raw_logsplits(stats_type,player_url):
    url = re.sub('.html','/' + stats_type + '/',player_url)
    page = requests.get("https://www.sports-reference.com" + url)
    if page.status_code == 404:
        return
    soup = BeautifulSoup(page.content,"html.parser")
    return soup.findAll('table')

def parse_rawstr(raw_str,pattern):
    str_dict = {}
    indexes = [(m.start(0), m.end(0)) for m in re.finditer(pattern, raw_str)]
    for i in range(0,len(indexes)):
        index = indexes[i]
        backetless_str = bracketstrip(raw_str[index[0]+1:index[1]-1])
        category = strip_raw_info(backetless_str)
        if i == len(indexes)-1:
            processed_str = raw_str[index[1]:]
        else:     
            processed_str = raw_str[index[1]:indexes[i+1][0]] 
        str_dict[category] = processed_str
    return str_dict
 
def cull_splits_table(splits_table):
    category_dict = parse_rawstr(str(splits_table),"data\-stat\=\"split\_id\" scope\=\"row\"\>\w+<\/th\>")
    for category in category_dict:
        category_data = category_dict[category]
        data_dict = parse_rawstr(category_data,"data-stat=\"split_value\">.*?</td>")
        for data in data_dict:
            data_dict[data] = sift_split(data_dict[data])
        category_dict[category] = data_dict
    return category_dict

def cull_gamelog_table(gamelog_table):
    log_dict = parse_rawstr(str(gamelog_table),"\>\d\d\d\d\-\d\d\-\d\d\<")
    for date in log_dict:
        log_dict[date] = sift_log(log_dict[date])
    return log_dict

def main():
    index_start = int(sys.argv[1])
    index_end = int(sys.argv[2]) 
     # length of url_list 113877
    con = attempt_connection()
    with con:
        cur = con.cursor()
        cur.execute("SELECT URL FROM SR_PLAYERS")
        url_list = cur.fetchall()
        for i in range(index_start,index_end):
            try:
                player_url = url_list[i]
                gamelog_table = get_raw_logsplits("gamelog", player_url[0])
                splits_table = get_raw_logsplits("splits", player_url[0])
                log_dict = cull_gamelog_table(gamelog_table)
                splits_dict = cull_splits_table(splits_table)
                splits_str = standardize_for_SQL(str(splits_dict))
                log_str = standardize_for_SQL(str(log_dict))
                cur.execute("UPDATE SR_PLAYERS SET GAMELOGS='%s', SPLITS='%s' WHERE URL = '%s'" % (log_str,splits_str,player_url[0]))
            except:
                print "ERROR: " + player_url[0]
    return 0;

if __name__ == "__main__":
    main()
