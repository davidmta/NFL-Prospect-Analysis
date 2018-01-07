import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv
import sqlite3 as lite
import os
import time
import httplib
from stats_scrape import parse_defense,parse_passing,rushing_receiving,punting_and_kicking,scoring,punt_kick_returns,strip_raw_info


def strip_position(raw_str):
    start = raw_str.find(':')
    return raw_str[start+2:len(raw_str)-5]

def strip_draft(draft):
    return re.sub('\<.*?\>','',draft)

def identifying_stats_match(pattern,page_content):
    match = re.search(pattern,page_content)
    if match != None:
        stat = match.group(0)
    else:
        stat = ""
    return stat

def get_identifying_stats(page_content):
    ## Position
    position = identifying_stats_match('Position<\/strong\>\:\s.*?\s\<\/p\>',page_content)
    position = strip_position(position)
    ## Draft
    draft = identifying_stats_match('\<p\>\<strong\>Draft\:\<\/strong\>.*?\<\/p\>',page_content)
    draft = strip_draft(draft)
    ## Height
    height = identifying_stats_match('itemprop\=\"height\"\>\d\-\d+\<\/span\>\,\&nbsp\;\<span',page_content)
    height = strip_raw_info(height)
    ## Weight  
    weight = identifying_stats_match('itemprop\=\"weight\"\>\d+lb\<\/span\>\&nbsp',page_content)
    weight = strip_raw_info(weight)    
    return position, draft, height, weight

def sift_for_stats(player_url,years_active,player_name):
    try:
        page = requests.get("https://www.sports-reference.com" + player_url)
    except:
        return "","","","",["","","","","",""]

    position, draft, height, weight = get_identifying_stats(page.content)

    pkreturn_stats = {}
    pk_stats = {}
    scoring_stats = {}
    rr_stats = {}
    pass_stats = {}
    def_stats = {}
    trs = re.findall('\<tr\s\>.*?\<\/tr\>',page.content)
    for tr in trs:
        if re.search('tackles_assists',tr) != None:
            def_stats = parse_defense(tr,def_stats)
        elif re.search('pass_att',tr) != None:
            pass_stats = parse_passing(tr,pass_stats)
        elif re.search('rush_att',tr) != None:
            rr_stats = rushing_receiving(tr,rr_stats)
        elif re.search('td_def_int',tr) != None:
            scoring_stats = scoring(tr,scoring_stats)
        elif re.search('punt_yds_per_punt',tr) != None:
            pk_stats = punting_and_kicking(tr,pk_stats)
        elif re.search('kick_ret_yds_per_ret',tr) != None:
            pkreturn_stats = punt_kick_returns(tr,pkreturn_stats)
    stats = [standardize_for_SQL(str(def_stats)),
            standardize_for_SQL(str(pass_stats)),
            standardize_for_SQL(str(rr_stats)),
            standardize_for_SQL(str(scoring_stats)),
            standardize_for_SQL(str(pk_stats)),
            standardize_for_SQL(str(pkreturn_stats))]
    return position,draft,height,weight,stats


def strip_raw_url(raw_url):
    return raw_url[12:]

def standardize_for_SQL(raw):
    return raw.replace('\'','\'\'')

def get_identification(p_str):
    url_result = re.search('\<p\>\<a href\=\"/cfb/players/\w+\-\w+\-\d.html',p_str)
    years_result = re.search('\(\d+\-\d+\)',p_str)
    name_result = re.search('\.html\"\>.*?\s.*?\<\/a\>',p_str)
    college_result = re.search('\/cfb\/schools\/.*?\/\"\>.*?\<\/a\>',p_str)
    return url_result, years_result, name_result, college_result

def get_players_stats(page,cur):
    soup = BeautifulSoup(page.content,"html.parser")
    p_soup = soup.findAll('p')
    
    for p in p_soup:
        url_result, years_result, name_result, college_result = get_identification(str(p))
        if url_result and years_result and name_result and college_result != None:
            years_active = years_result.group(0)
            player_url = strip_raw_url(url_result.group(0))
            player_name = strip_raw_info(name_result.group(0))
            player_name = standardize_for_SQL(player_name)
            college = strip_raw_info(college_result.group(0))
            college = standardize_for_SQL(player_name)
            print player_name
            print player_url
            position,draft,height,weight,stats = sift_for_stats(player_url,years_active,player_name)
            cur.execute("INSERT INTO SR_PLAYERS VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (player_name,player_url,college,years_active,position,height,weight,draft,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],"",""))
                        
def get_data(cur,start,end):
    for letter in range(ord(start),ord(end)+1):
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index" + ".html")
        get_players_stats(page,cur)
        page_index = 2
        while(page.status_code != 404):
            page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index-" + str(page_index) + ".html")
            if page.status_code != 404:
                get_players_stats(page,cur)
                page_index = page_index + 1

def attempt_connection(start,end):
    try:
        con = lite.connect('sr_players_database_' + start + '_' + end + '.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE SR_PLAYERS(PLAYER TEXT,URL TEXT,COLLEGE TEXT,YEARS_ACTIVE TEXT,POSITION TEXT,HEIGHT TEXT,WEIGHT TEXT,DRAFT TEXT,DEFENSE_AND_FUMBLES TEXT,PASSING TEXT,RUSHING_AND_RECEIVING TEXT,SCORING TEXT,PUNTING_AND_KICKING TEXT,PUNT_AND_KICK_RETURNS TEXT,GAMELOGS TEXT,SPLITS TEXT)")

def main():
    start = sys.argv[1]
    end = sys.argv[2] 
    con = attempt_connection(start,end)
    with con:
        cur = con.cursor()
        create_table(cur)
        get_data(cur,start,end)
    # return 0;

if __name__ == "__main__":
    main()
